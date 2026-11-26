from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class Decompose(BaseModel):
    model_config = ConfigDict(extra="forbid")
    window_code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]


class ClassifyPulse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    token: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    action: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
