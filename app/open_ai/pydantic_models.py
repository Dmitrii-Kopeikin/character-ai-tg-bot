from typing import List
from pydantic import BaseModel


class MessageModel(BaseModel):
    role: str
    content: str


class RequestModel(BaseModel):
    model: str
    messages: List[MessageModel]
    user: int


class ChoiceModel(BaseModel):
    index: int
    message: MessageModel
    finish_reason: str


class UsageModel(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ResponseModel(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: List[ChoiceModel]
    usage: UsageModel
