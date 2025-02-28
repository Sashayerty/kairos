import json
import time

import colorama

# import markdown
from flask import Blueprint, render_template, request

from app.ai_core import censor, cool_prompt, get_theory, plan

ai_couch = Blueprint(
    "ai_couch",
    __name__,
    template_folder="../templates/ai_couch",
)
colorama.init(autoreset=True)


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
    users_desires = dict(request.form.items())["users_desires"]
    print(f" * User's theme: {users_theme}")
    if users_desires:
        print(f" * User's desires: {users_desires}")
    answer_from_censor = json.loads(
        censor(theme_from_user=users_theme, desires=users_desires)
    )
    is_theme_are_good = answer_from_censor["data"]
    print(f" * User's theme is good: {is_theme_are_good}")
    time.sleep(1)
    message = answer_from_censor["reason"] if not is_theme_are_good else None
    if message:
        print(message)
        return render_template(
            "index.html", message=message, title="Kairos - Главная"
        )
    else:
        prompt_from_llm = cool_prompt(
            users_theme=users_theme,
            desires=users_desires,
        )
        print(prompt_from_llm)
        time.sleep(1)
        plan_of_course: dict = json.loads(
            plan(prompt_from_llm=prompt_from_llm)
        )
        print(colorama.Fore.GREEN + " * Plan of course created successfully!")
        print(plan_of_course)
        time.sleep(1)
        course = get_theory(
            prompt_from_prompt_agent=prompt_from_llm,
            plan=plan_of_course,
        )
        print(" * Course function invoked successfully!")
        if course:
            print(colorama.Fore.GREEN + " * Course created successfully!")
        return render_template(
            "course.html", course=json.loads(course), title="Kairos - Курс"
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
