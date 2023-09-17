import json
import logging
from typing import Any, Dict

import httpx
import openai
import tiktoken
from pydantic import ValidationError

from app.utils.singleton_meta import SingletonMeta
from config import config

from .pydantic_models import RequestModel, ResponseModel

logger = logging.getLogger(__name__)


class OpenAiException(Exception):
    pass


class OpenAI(metaclass=SingletonMeta):
    def __init__(self):
        self.gateway = config.open_ai.gateway
        self.api_key = config.open_ai.api_key

        self.model = config.open_ai.model
        self.max_tokens = config.open_ai.max_tokens
        self.context_requests_count = config.open_ai.context_requests_count

        self.encoding = tiktoken.encoding_for_model(self.model)

        openai.api_key = self.api_key

    async def request_http(
        self,
        prompt: str,
        context: str,
        user_message: str,
        user_id: int,
    ) -> Dict[str, Any]:
        system_message = self.create_system_message(
            prompt=prompt,
            context=context,
            request=user_message,
        )

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
            "Authorization": f"Bearer {self.api_key}",
        }
        data = {
            "model": self.model,
            "messages": messages,
            "user": str(user_id),
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

                logger.info(result.json())

                data = ResponseModel.model_validate(result.json())
                return data.model_dump()
            except Exception as e:
                logger.warning(e)
                logger.warning("Trying to do request again.")
                attempt += 1

        logger.error("Failed to request.")
        raise OpenAiException("Failed to request.")

    async def request(
        self,
        prompt: str,
        context: str,
        user_message: str,
        user_id: int,
    ) -> Dict[str, Any]:
        system_message = self.create_system_message(
            prompt=prompt,
            context=context,
            request=user_message,
        )

        completion = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
            user=str(user_id),
        )

        response = dict(completion)
        return response

    def create_system_message(
        self,
        prompt: str,
        context: str,
        request: str,
    ) -> str:
        prompt_tokens = self.encoding.encode(prompt)
        context_tokens = self.encoding.encode(context)
        request_tokens = self.encoding.encode(request)

        if (
            len(prompt_tokens) + len(context_tokens) + len(request_tokens)
            > self.max_tokens
        ):
            slice_index = self.max_tokens - (
                len(prompt_tokens) + len(request_tokens)
            )
            context = self.encoding.decode(context_tokens[slice_index:])

        return f"prompt: {prompt}\ncontext: {context}"


open_ai = OpenAI()
