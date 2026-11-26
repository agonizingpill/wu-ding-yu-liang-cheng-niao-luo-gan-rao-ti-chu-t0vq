from typing import Annotated

from pydantic import BaseModel, ConfigDict, FiniteFloat, StringConstraints

class TareScale(BaseModel):
    model_config = ConfigDict(extra="forbid")
    gauge: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    check: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
