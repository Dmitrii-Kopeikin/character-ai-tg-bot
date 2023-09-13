from typing import Callable

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.utils.singleton_meta import SingletonMeta

from .routers import webapp_router


class WebApp(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self.app = FastAPI()

        self.app.mount(
            "/static",
            StaticFiles(directory="app/web/static"),
            name="static",
        )

        self.app.include_router(webapp_router)

    def add_route(
        self,
        func: Callable,
        path: str,
        method: str,
    ) -> None:
        self.app.add_api_route(path=path, endpoint=func, methods=[method])

    def add_start_event_handler(
        self,
        func: Callable,
    ) -> None:
        self.app.add_event_handler("startup", func)

    def add_shutdown_event_handler(
        self,
        func: Callable,
    ) -> None:
        self.app.add_event_handler("shutdown", func)
