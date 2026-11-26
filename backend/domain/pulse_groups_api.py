from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import pulse_groups_service as service
from domain.pulse_groups_model import pulse_groups
from domain.pulse_groups_schemas import OpenReview, CancelReview, IssueReview

router = APIRouter()

@router.get('/pulse_groups')
def list_pulse_groups(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, pulse_groups)


@router.post('/pulse_groups/open-review')
def open_review(data: OpenReview, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.open_review(conn, user, data)
        record(conn, user, 'pulse_groups.open_review')
        return output


@router.post('/pulse_groups/cancel-review')
def cancel_review(data: CancelReview, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.cancel_review(conn, user, data)
        record(conn, user, 'pulse_groups.cancel_review')
        return output


@router.post('/pulse_groups/issue-review')
def issue_review(data: IssueReview, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.issue_review(conn, user, data.code, data.rain)
        record(conn, user, 'pulse_groups.issue_review')
        return output
