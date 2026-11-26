from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, StringConstraints

class PublishRain(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
    flag: Optional[Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]] = None
    group: Optional[Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=64)]] = None
