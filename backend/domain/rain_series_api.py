from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import rain_series_service as service
from domain.rain_series_model import rain_series
from domain.rain_series_schemas import PublishRain

router = APIRouter()

@router.get('/rain_series')
def list_rain_series(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, rain_series)


@router.post('/rain_series/publish-rain')
def publish_rain(data: PublishRain, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.publish_rain(conn, user, data)
        record(conn, user, 'rain_series.publish_rain')
        return output
