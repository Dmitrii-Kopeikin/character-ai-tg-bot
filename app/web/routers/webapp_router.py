from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.database.dal import character_dal, conversation_dal, user_dal

from ..dependencies import (
    get_amplitude_client,
    get_bot,
    get_session,
    get_templates,
)

webapp_router = APIRouter(include_in_schema=False)


@webapp_router.get("/choose_character", response_class=HTMLResponse)
async def choose_character(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
) -> HTMLResponse:
    characters = await character_dal.get_all()

    characters_list = []

    for character in characters:
        characters_list.append(
            {
                "id": character.id,
                "name": character.name,
                "image": character.image,
                "description": character.description,
            }
        )

    return templates.TemplateResponse(
        "choose_character.html",
        {
            "request": request,
            "characters": characters_list,
        },
    )


@webapp_router.post("/choose_character", response_class=JSONResponse)
async def character_chosen(
    request: Request,
    bot=Depends(get_bot),
    amplitude_client=Depends(get_amplitude_client),
    session=Depends(get_session),
):
    data = await request.json()

    user_tg_id = int(data["user_tg_id"])
    character_id = int(data["character_id"])

    user = await user_dal.get(tg_id=user_tg_id, session=session)
    character = await character_dal.get(id=character_id, session=session)

    if not all((user, character)):
        await bot.send_message(
            text="Произошла ошибка. Попробуйте еще раз.",
            chat_id=user_tg_id,
        )
        return {"success": False}

    amplitude_client.track_character_selection(
        user_id=user.id,
        data={
            "user_tg_id": user_tg_id,
            "character_id": character_id,
        },
    )

    conversation = await conversation_dal.create(
        character_id=character_id,
        user_id=user.id,
        session=session,
    )
    await user_dal.update(
        id=user.id,
        current_conversation_id=conversation.id,
        session=session,
    )

    await session.commit()

    await bot.send_message(
        text=character.greetings,
        chat_id=user_tg_id,
    )
    return {"success": True}
