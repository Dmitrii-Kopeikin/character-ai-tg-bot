import inspect
from typing import Annotated, Type

from fastapi import Form
from pydantic import BaseModel, Field


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


def as_form(cls):
    new_params = [
        inspect.Parameter(
            field_name,
            inspect.Parameter.POSITIONAL_ONLY,
            default=model_field.default,
            annotation=Annotated[
                model_field.annotation, *model_field.metadata, Form()
            ],
        )
        for field_name, model_field in cls.model_fields.items()
    ]

    cls.__signature__ = cls.__signature__.replace(parameters=new_params)

    return cls
