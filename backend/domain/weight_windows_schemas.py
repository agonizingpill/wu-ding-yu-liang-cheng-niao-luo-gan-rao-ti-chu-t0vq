from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class NoteWindow(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    gauge: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    probes: list | dict
    rain_mm: FiniteFloat


class ProtectWindow(BaseModel):
    model_config = ConfigDict(extra="forbid")
    window_code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    protected: bool
