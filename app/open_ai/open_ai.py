import json
import logging
from typing import Any, Dict

import httpx

from app.utils.singleton_meta import SingletonMeta
from config import config

from .pydantic_models import RequestModel, ResponseModel
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class OpenAiException(Exception):
    pass


class OpenAI(metaclass=SingletonMeta):
    def __init__(self):
        self.gateway = config.open_ai.gateway
        self.api_key = config.open_ai.api_key

    async def request_by_gateway(
        self,
        system_message: str,
        user_message: str,
    ) -> Dict[str, Any]:
        messages = [
            {
                "role": "system",
                "content": system_message,
            },
            {
                "role": "user",
                "content": user_message,
            },
        ]
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
        }

        try:
            RequestModel.model_validate(data)
        except ValidationError as e:
            raise OpenAiException(e.errors())

        attempt = 1

        while attempt <= config.open_ai.request_attempts:
            try:
                async with httpx.AsyncClient() as client:
                    timeout = httpx.Timeout(120.0, read=None)
                    result = await client.post(
                        url=self.gateway,
                        headers=headers,
                        data=json.dumps(data),
                        timeout=timeout,
                    )

                data = ResponseModel.model_validate(result.json())
                return data.model_dump()
            except Exception as e:
                logger.warning(e)
                logger.warning("Trying to do request again.")
                attempt += 1

        logger.error("Failed to request.")
        raise OpenAiException("Failed to request.")


open_ai = OpenAI()
