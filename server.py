import flask
from flask import jsonify, request
from flask.views import MethodView
from models import Advertisement, Session
from sqlalchemy.exc import IntegrityError
from schema import CreateAdv, UpdateAdv
from pydantic import ValidationError


app = flask.Flask("app")


class HttpError(Exception):

    def __init__(self, status_code: int, error_msg: str | list | dict):
        self.status_code = status_code
        self.error_msg = error_msg


@app.errorhandler(HttpError)
def http_error_handler(err: HttpError):
    http_response = jsonify({"status": "error", "massage": err.error_msg})
    http_response.status = err.status_code
    return http_response


def validate_json(json_data: dict, schema_cls: type[CreateAdv] | type[UpdateAdv]):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop("ctx", None)
        raise HttpError(400, errors)


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(http_response: flask.Response):
    request.session.close
    return http_response


def add_adv(adv: Advertisement):
    try:
        request.session.add(adv)
        request.session.commit()
        return adv
    except IntegrityError:
        request.session.rollback()
        raise HttpError(400, "Поле не должно быть пустым")


def get_adv(adv_id: int):
    adv = request.session.get(Advertisement, adv_id)
    if adv is None:
        raise HttpError(404, "Обьявление не найдено")
    return adv


class AdvertisementView(MethodView):

    def post(self):
        json_data = validate_json(request.json, CreateAdv)
        adv = Advertisement(**json_data)
        adv = add_adv(adv)
        return jsonify({'id': adv.id}), 201

    def delete(self, adv_id: int):
        adv = get_adv(adv_id)
        request.session.delete(adv)
        request.session.commit()
        return jsonify({'message': 'Объявление успешно удалено'}), 200

    def get(self, adv_id: int):
        adv = get_adv(adv_id)
        return jsonify(adv.json)

    def patch(self, adv_id: int):
        json_data = validate_json(request.json, UpdateAdv)
        adv = get_adv(adv_id)
        for key, value in json_data.items():
            setattr(adv, key, value)
        request.session.commit()
        return jsonify(adv.json)


advertisement_view = AdvertisementView.as_view('advertisement')

app.add_url_rule("/advertisement/", view_func=advertisement_view, methods=["POST"])
app.add_url_rule("/advertisement/<int:adv_id>/", view_func=advertisement_view, methods=["DELETE", "PATCH", "GET"])

if __name__ == '__main__':
    app.run()
