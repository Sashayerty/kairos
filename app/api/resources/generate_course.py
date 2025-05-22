import json

from flask_restful import Resource, reqparse

from app.agents import check, gen_course, gen_plan, gen_prompt

parser = reqparse.RequestParser()


class GenerateCourse(Resource):
    def post(self):
        """Генерация курса. Подробнее ../docs/restapi.md"""
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
            check(
                theme=users_theme,
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
        prompt_from_llm = gen_prompt(
            theme=users_theme,
            desires=users_desires,
            description_of_user=description_of_user,
        )
        plan_of_course: dict = json.loads(gen_plan(prompt=prompt_from_llm))
        course = gen_course(
            prompt=prompt_from_llm,
            plan=plan_of_course,
        )
        return {
            "theme": users_theme,
            "desires": users_desires,
            "description_of_user": description_of_user,
            "answer_from_censor": answer_from_censor,
            "prompt": prompt_from_llm,
            "plan": plan_of_course,
            "course": course,
        }, 200
