from fastapi import UploadFile
from pydantic import BaseModel
from .decorators import as_form


@as_form
class CreateCharacterSchema(BaseModel):
    name: str
    description: str
    greetings: str
    image: UploadFile
    prompt: str
