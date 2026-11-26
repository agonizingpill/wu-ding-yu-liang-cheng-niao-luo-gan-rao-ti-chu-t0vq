from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.roof_gauges_model import roof_gauges
from domain.weight_windows_model import weight_windows
from domain.artifact_flags_model import artifact_flags
from domain.rain_series_model import rain_series


def decompose(conn, user, data):
    row=get(conn,weight_windows,data.window_code)
    history=[x for x in scan(conn,weight_windows) if x['gauge']==row['gauge'] and
             x['code']!=row['code'] and x['state']=='已登记']
    need(len(history)>=30,'至少需要同秤架三十窗基线')
    return submit(user,{'target':row,'baseline':history})


def classify_pulse(conn, user, data):
    run=result(user,data.token)
    metrics=run['result']
    target=get(conn,weight_windows,run['input']['target']['code'],lock=True)
    need(target['state']=='已登记','观测窗此前已有处置')
    need(data.action in ('保留','排除'),'选择保留或排除')
    if data.action=='排除':
        need(not target['protected'],'人工保留窗口禁止剔除')
        need(metrics['score']>metrics['cutoff'],'无足够残差证据剔除')
    row=insert(conn,artifact_flags,code=data.code,window_code=target['code'],score=metrics['score'],
        limit_value=metrics['cutoff'],action=data.action,token=data.token)
    update(conn,weight_windows,target['code'],state='脉冲排除' if data.action=='排除' else '人工保留')
    return row
