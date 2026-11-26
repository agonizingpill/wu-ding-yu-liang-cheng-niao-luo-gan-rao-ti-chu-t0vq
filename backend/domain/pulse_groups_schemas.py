from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

WindowCode = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]
GroupCode = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=64)]
RainCode = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=160)]


class OpenReview(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: GroupCode
    windows: Annotated[list[WindowCode], Field(min_length=1)]


class CancelReview(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: GroupCode


class IssueReview(BaseModel):
    model_config = ConfigDict(extra="forbid")
    code: GroupCode
    rain: RainCode
