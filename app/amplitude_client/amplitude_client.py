import logging
from typing import Any, Dict

from amplitude import Amplitude, BaseEvent, Config

from app.utils.singleton_meta import SingletonMeta
from config import config


class AmplitudeClient(metaclass=SingletonMeta):
    amplitude_client: Amplitude

    def __init__(self) -> None:
        amplitude_config = Config(
            logger=logging.getLogger("Amplitude"),
            min_id_length=1,
        )

        self.amplitude_client = Amplitude(
            api_key=config.amplitude.api_key,
            configuration=amplitude_config,
        )

    def track_registration(
        self,
        user_id: int,
        data: Dict[str, Any],
    ):
        print("Trying to track registration...")
        self.amplitude_client.track(
            BaseEvent(
                event_type="registration",
                user_id=str(user_id),
                event_properties=data,
            )
        )

    def track_character_selection(
        self,
        user_id: int,
        data: Dict[str, Any],
    ):
        self.amplitude_client.track(
            BaseEvent(
                event_type="character_selection",
                user_id=str(user_id),
                event_properties=data,
            )
        )

    def track_request(
        self,
        user_id: int,
        data: Dict[str, Any],
    ):
        self.amplitude_client.track(
            BaseEvent(
                event_type="ai_request",
                user_id=str(user_id),
                event_properties=data,
            )
        )

    def track_response(
        self,
        user_id: int,
        data: Dict[str, Any],
    ):
        self.amplitude_client.track(
            BaseEvent(
                event_type="ai_response",
                user_id=str(user_id),
                event_properties=data,
            )
        )

    def track_response_sent_to_user(
        self,
        user_id: int,
        data: Dict[str, Any],
    ):
        self.amplitude_client.track(
            BaseEvent(
                event_type="response_sent_to_user",
                user_id=str(user_id),
                event_properties=data,
            )
        )

    def shutdown(self):
        self.amplitude_client.shutdown()


amplitude_client = AmplitudeClient()
