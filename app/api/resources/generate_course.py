import json

from flask_restful import Resource, reqparse

from app.ai_core import censor, cool_prompt, get_theory, plan

parser = reqparse.RequestParser()


class GenerateCourse(Resource):
    def post(self):
        parser.add_argument(
            name="theme",
            type=str,
            location="json",
            required=True,
        )
        parser.add_argument(
            name="desires",
            type=str,
            location="json",
        )
        parser.add_argument(
            name="description_of_user",
            type=str,
            location="json",
        )
        args = parser.parse_args()
        users_theme = args.theme
        users_desires = args.desires
        description_of_user = args.description_of_user
        answer_from_censor = json.loads(
            censor(
                theme_from_user=users_theme,
                desires=users_desires,
            )
        )
        is_theme_are_good = answer_from_censor["data"]
        message = (
            answer_from_censor["reason"] if not is_theme_are_good else None
        )
        if not is_theme_are_good:
            return {
                "message": message,
                "theme_is_good": False,
            }, 400
        prompt_from_llm = cool_prompt(
            users_theme=users_theme,
            desires=users_desires,
            description_of_user=description_of_user,
        )
        plan_of_course: dict = json.loads(
            plan(prompt_from_llm=prompt_from_llm)
        )
        course = json.loads(
            get_theory(
                prompt_from_prompt_agent=prompt_from_llm,
                plan=plan_of_course,
            )
        )
        return {
            "theme": users_theme,
            "desires": users_desires,
            "description_of_user": description_of_user,
            "answer_from_censor": answer_from_censor,
            "prompt_from_llm": prompt_from_llm,
            "plan_of_course": plan_of_course,
            "course": course,
        }, 200
