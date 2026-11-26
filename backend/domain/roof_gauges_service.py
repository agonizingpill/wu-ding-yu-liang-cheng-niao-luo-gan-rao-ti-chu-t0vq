from sqlalchemy import select

from core.queueing import submit, result
from core.records import get, insert, need, scan, update
from domain.roof_gauges_model import roof_gauges
from domain.weight_windows_model import weight_windows
from domain.artifact_flags_model import artifact_flags
from domain.rain_series_model import rain_series


def tare_scale(conn, user, data):
    get(conn,roof_gauges,data.gauge,lock=True)
    need(data.check.startswith('TARE-'),'需要纸本归零凭记')
    return update(conn,roof_gauges,data.gauge,tared=True)
