from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.roof_gauges_model import roof_gauges
from domain.weight_windows_model import weight_windows
from domain.artifact_flags_model import artifact_flags
from domain.rain_series_model import rain_series


def note_window(conn, user, data):
    gauge=get(conn,roof_gauges,data.gauge,lock=True)
    need(gauge['tared'],'秤架尚未归零')
    need(isinstance(data.probes,list) and len(data.probes)==3 and
         all(type(x) in (int,float) and -100<=x<=100 for x in data.probes),'须录入三路有限读数')
    need(0<=data.rain_mm<=150,'折算雨量超出窗口量程')
    return insert(conn,weight_windows,**data.model_dump(),protected=False,state='已登记')


def protect_window(conn, user, data):
    row=get(conn,weight_windows,data.window_code,lock=True)
    need(row['state']=='已登记','已处理的雨窗需另开复查')
    return update(conn,weight_windows,data.window_code,protected=data.protected)
