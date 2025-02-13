from pydantic import BaseModel
from typing import Optional


class Message(BaseModel):
    role: str
    content: str
    refusal: Optional[str] = None


class Choice(BaseModel):
    logprobs: Optional[dict] = None
    finish_reason: str
    native_finish_reason: str
    index: int
    message: Message


class MistralLlmResponse(BaseModel):
    id: str
    provider: str
    model: str
    object: str
    created: int
    choices: list[Choice]
