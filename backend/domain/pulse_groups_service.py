from uuid import uuid4

from sqlalchemy import select

from core.records import get, insert, need, scan, update
from domain.artifact_flags_model import artifact_flags
from domain.learning import score_group
from domain.pulse_groups_model import pulse_groups
from domain.rain_series_model import rain_series
from domain.roof_gauges_model import roof_gauges
from domain.weight_windows_model import weight_windows

OPEN = '复核中'
CANCELLED = '已撤销'
ISSUED = '已签发'
MIN_BASELINE = 30


def _present(conn, table, code):
    return conn.execute(select(table.c.code).where(table.c.code == code)).first() is not None


def open_group_on_gauge(conn, gauge):
    rows = conn.execute(select(pulse_groups).where(pulse_groups.c.gauge == gauge,
                                                    pulse_groups.c.status == OPEN)).mappings().all()
    return dict(rows[0]) if rows else None


def open_review(conn, user, data):
    need(not _present(conn, pulse_groups, data.code), '复核组编号已存在')
    codes = list(dict.fromkeys(data.windows))
    need(len(codes) == len(data.windows), '圈选的嫌疑窗有重复')
    rows = []
    for code in codes:
        row = get(conn, weight_windows, code)
        need(row['state'] == '已登记', '嫌疑窗此前已有处置')
        rows.append(row)
    gauges = {row['gauge'] for row in rows}
    need(len(gauges) == 1, '圈选窗口须来自同一秤架')
    gauge = get(conn, roof_gauges, gauges.pop(), lock=True)
    # 同秤只允许一组未结复核，否则后来的基线会把前一组的嫌疑窗重新混入
    need(open_group_on_gauge(conn, gauge['code']) is None, '该秤架已有未结复核组')
    baseline = [x for x in scan(conn, weight_windows)
                if x['gauge'] == gauge['code'] and x['state'] == '已登记' and x['code'] not in codes]
    need(len(baseline) >= MIN_BASELINE, '至少需要同秤架三十窗组外基线')
    scores, limit = score_group(baseline, rows)
    return insert(conn, pulse_groups, code=data.code, gauge=gauge['code'], windows=codes,
                  baseline=[x['code'] for x in baseline], scores=scores, limit_value=limit,
                  status=OPEN, flag=None, rain=None)


def cancel_review(conn, user, data):
    group = get(conn, pulse_groups, data.code, lock=True)
    need(group['status'] == OPEN, '仅未结案的复核可撤销')
    return update(conn, pulse_groups, data.code, status=CANCELLED)


def issue_review(conn, user, group_code, rain_code):
    """整组排除与雨列签发在同一事务内生效。重复签发返回既有雨列，不新增雨列。"""
    group = get(conn, pulse_groups, group_code, lock=True)
    if group['rain'] is not None:
        return get(conn, rain_series, group['rain'])
    need(group['status'] == OPEN, '仅未结案的复核可整组签发')
    gauge = get(conn, roof_gauges, group['gauge'], lock=True)
    codes = group['windows']
    scores = group['scores'] or {}
    limit = group['limit_value']
    # 统一加锁顺序（秤架 -> 各嫌疑窗），与人工保留的加锁串行化
    windows = [get(conn, weight_windows, code, lock=True) for code in sorted(codes)]
    need(all(w['gauge'] == gauge['code'] for w in windows), '嫌疑窗秤架与复核组不符')
    # 任一窗已被处置、被人工保留或没过剔除线，整组退回，不留部分排除
    need(all(w['state'] == '已登记' for w in windows), '嫌疑窗此前已有处置，整组退回')
    for w in windows:
        need(not w['protected'], '嫌疑窗已被人工保留，整组退回')
        need(float(scores.get(w['code'], float('-inf'))) > float(limit),
             '存在未过剔除线的嫌疑窗，整组退回')
    need(not _present(conn, rain_series, rain_code), '雨列编号已存在')
    flags = []
    for w in windows:
        flag = 'PULSE-' + uuid4().hex
        insert(conn, artifact_flags, code=flag, window_code=w['code'],
               score=float(scores[w['code']]), limit_value=float(limit),
               action='排除', token=uuid4().hex)
        update(conn, weight_windows, w['code'], state='脉冲排除')
        flags.append(flag)
    rows = [x for x in scan(conn, weight_windows) if x['gauge'] == gauge['code']]
    valid = [x for x in rows if x['state'] != '脉冲排除']
    rain = insert(conn, rain_series, code=rain_code, gauge=gauge['code'], flag=flags[0],
                  total=round(sum(x['rain_mm'] for x in valid), 3), n_windows=len(valid),
                  omitted=len(rows) - len(valid))
    update(conn, pulse_groups, group_code, status=ISSUED, flag=flags[0], rain=rain_code)
    return rain
