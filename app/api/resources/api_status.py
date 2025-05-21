from http import HTTPStatus

from flask_restful import Resource


class ApiStatus(Resource):
    def get(self):
        """Возвращает статус запуска RestAPI"""
        return {"details": "Kairos server is running!"}, HTTPStatus.OK
