from sqlalchemy import select

from core.records import get, insert, need, scan, update
from domain.roof_gauges_model import roof_gauges
from domain.weight_windows_model import weight_windows
from domain.artifact_flags_model import artifact_flags
from domain.rain_series_model import rain_series
from domain import pulse_groups_service


def publish_rain(conn, user, data):
    if data.group:
        # 整组排除与雨列签发在同一事务内一同生效；重试返回既有雨列，不新增
        return pulse_groups_service.issue_review(conn, user, data.group, data.code)
    need(data.flag, '请提供复核签条或整组复核号')
    review=get(conn,artifact_flags,data.flag)
    source=get(conn,weight_windows,review['window_code'])
    gauge=get(conn,roof_gauges,source['gauge'],lock=True)
    # 同秤有未结复核时，旧签条暂缓签发；撤销复核后解封
    need(pulse_groups_service.open_group_on_gauge(conn, gauge['code']) is None,'同秤复核未结案，旧签条暂缓签发')
    need(conn.execute(select(rain_series.c.code).where(rain_series.c.code==data.code)).first() is None,'雨列编号已存在')
    rows=[x for x in scan(conn,weight_windows) if x['gauge']==gauge['code']]
    valid=[x for x in rows if x['state']!='脉冲排除']
    return insert(conn,rain_series,**data.model_dump(exclude={'group'}),gauge=gauge['code'],
                  total=round(sum(x['rain_mm'] for x in valid),3),n_windows=len(valid),omitted=len(rows)-len(valid))
