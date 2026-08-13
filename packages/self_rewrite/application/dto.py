from pydantic import BaseModel, Field

"""Data Transfer Objects for Self Rewrite context."""


class SelfRewriteRequest(BaseModel):
    problem: str = Field(..., description="Problem statement to resolve")
    author: str = Field(..., description="Author or agent role")
