"""Data Transfer Objects for Self Rewrite context."""

from pydantic import BaseModel, Field


class SelfRewriteRequest(BaseModel):
    problem: str = Field(..., description="Problem statement to resolve")
    author: str = Field(..., description="Author or agent role")
