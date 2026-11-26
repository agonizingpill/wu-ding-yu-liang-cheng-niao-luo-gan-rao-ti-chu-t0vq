from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import roof_gauges_service as service
from domain.roof_gauges_model import roof_gauges
from domain.roof_gauges_schemas import TareScale

router = APIRouter()

@router.get('/roof_gauges')
def list_roof_gauges(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, roof_gauges)


@router.post('/roof_gauges/tare-scale')
def tare_scale(data: TareScale, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.tare_scale(conn, user, data)
        record(conn, user, 'roof_gauges.tare_scale')
        return output
