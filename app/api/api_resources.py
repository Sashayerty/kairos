# import http

import json

from flask_restful import Resource, abort, reqparse

from app.ai_core import censor, cool_prompt, edit_course, get_theory, plan

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
        args = parser.parse_args()
        users_theme = args.theme
        users_desires = args.desires
        answer_from_censor = json.loads(
            censor(theme_from_user=users_theme, desires=users_desires)
        )
        is_theme_are_good = answer_from_censor["data"]
        message = (
            answer_from_censor["reason"] if not is_theme_are_good else None
        )
        if not is_theme_are_good:
            return {
                "message": message,
            }, 400
        return {
            "theme": users_theme,
            "desires": users_desires,
            "answer_from_censor": answer_from_censor,
        }
