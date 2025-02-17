import json
import time

import markdown
from flask import Blueprint, render_template, request

from app.ai_core import censor, cool_prompt, plan

ai_couch = Blueprint(
    "ai_couch",
    __name__,
    template_folder="../templates/ai_couch",
)


@ai_couch.route(
    "/",
    methods=[
        "POST",
        "GET",
    ],
)
def index():
    return render_template("index.html", title="Kairos - Главная")


@ai_couch.route(
    "/create-course",
    methods=[
        "POST",
        "GET",
    ],
)
def create_course():
    users_theme = dict(request.form.items())["users_theme"]
    print(users_theme)
    is_theme_are_good = json.loads(censor(theme_from_user=users_theme))["data"]
    print(is_theme_are_good)
    time.sleep(1)
    message = (
        "Тема не прошла валидацию! Попробуйте сменить тему!"
        if not is_theme_are_good
        else None
    )
    if message:
        print(message)
        return render_template(
            "index.html", message=message, title="Kairos - Главная"
        )
    else:
        prompt_from_llm = cool_prompt(users_theme=users_theme)
        time.sleep(1)
        plane_of_course: dict = json.loads(
            plan(prompt_from_llm=prompt_from_llm)
        )
        keys_of_plane = plane_of_course.keys()
        plane_as_list = []
        for i in keys_of_plane:
            plane_as_list.append(f"{i} - {plane_of_course[i]}")
        plane = markdown.markdown("\n\n".join(plane_as_list))
        return render_template(
            "course.html",
            plane=plane,
        )


@ai_couch.route(
    "/course",
    methods=[
        "POST",
        "GET",
    ],
)
def course():
    pass
