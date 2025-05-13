import json

from flask_restful import Resource, reqparse

from app.agents import check

parser = reqparse.RequestParser()


class Check(Resource):
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
                "theme_is_good": is_theme_are_good,
            }, 400
        return {
            "message": "Theme is good",
            "theme_is_good": is_theme_are_good,
        }, 200
