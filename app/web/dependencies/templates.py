from typing import Any

from fastapi.templating import Jinja2Templates
from fastapi import Request


def url_for_https(request: Request, name: str, **path_params: Any) -> str:
    http_url = request.url_for(name, **path_params)
    https_url = http_url.replace("http", "https", 1)

    return https_url


def get_templates() -> Jinja2Templates:
    return templates


templates = Jinja2Templates(directory="app/web/templates", auto_reload=True)
templates.env.globals["url_for_https"] = url_for_https
