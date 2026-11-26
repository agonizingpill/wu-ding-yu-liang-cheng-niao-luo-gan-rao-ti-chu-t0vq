from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import artifact_flags_service as service
from domain.artifact_flags_model import artifact_flags
from domain.artifact_flags_schemas import Decompose, ClassifyPulse

router = APIRouter()

@router.get('/artifact_flags')
def list_artifact_flags(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, artifact_flags)


@router.post('/artifact_flags/decompose')
def decompose(data: Decompose, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.decompose(conn, user, data)
        record(conn, user, 'artifact_flags.decompose')
        return output


@router.post('/artifact_flags/classify-pulse')
def classify_pulse(data: ClassifyPulse, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.classify_pulse(conn, user, data)
        record(conn, user, 'artifact_flags.classify_pulse')
        return output
