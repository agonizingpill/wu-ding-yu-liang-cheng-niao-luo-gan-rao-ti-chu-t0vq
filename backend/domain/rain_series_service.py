from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.roof_gauges_model import roof_gauges
from domain.weight_windows_model import weight_windows
from domain.artifact_flags_model import artifact_flags
from domain.rain_series_model import rain_series


def publish_rain(conn, user, data):
    review=get(conn,artifact_flags,data.flag)
    source=get(conn,weight_windows,review['window_code'])
    gauge=get(conn,roof_gauges,source['gauge'],lock=True)
    rows=[x for x in scan(conn,weight_windows) if x['gauge']==gauge['code']]
    valid=[x for x in rows if x['state']!='脉冲排除']
    return insert(conn,rain_series,**data.model_dump(),gauge=gauge['code'],
                  total=round(sum(x['rain_mm'] for x in valid),3),n_windows=len(valid),omitted=len(rows)-len(valid))
