from fastapi import APIRouter, Depends

from core.auth import actor, allow
from core.audit import record
from core.db import transaction
from core.records import scan
from domain import weight_windows_service as service
from domain.weight_windows_model import weight_windows
from domain.weight_windows_schemas import NoteWindow, ProtectWindow

router = APIRouter()

@router.get('/weight_windows')
def list_weight_windows(user=Depends(actor)):
    with transaction() as conn:
        return scan(conn, weight_windows)


@router.post('/weight_windows/note-window')
def note_window(data: NoteWindow, user=Depends(actor)):
    allow(user, ('operator', 'reviewer'))
    with transaction() as conn:
        output = service.note_window(conn, user, data)
        record(conn, user, 'weight_windows.note_window')
        return output


@router.post('/weight_windows/protect-window')
def protect_window(data: ProtectWindow, user=Depends(actor)):
    allow(user, ('reviewer',))
    with transaction() as conn:
        output = service.protect_window(conn, user, data)
        record(conn, user, 'weight_windows.protect_window')
        return output
