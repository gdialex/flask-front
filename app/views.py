from app import app, USERS, models
from flask import request, Response
import json
from http import HTTPStatus
@app.route("/")
def index():
    return "<h1>Hello world</h1>"


@app.post("/user/create")
def user_create():
    data = request.get_json()
    id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    email = data["email"]

    # todo: check the phone and email for validity

    user = models.User(id, first_name, last_name, phone, email)
    USERS.append(user)
    response = Response(
        json.dumps({
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone": user.phone,
            "email": user.email,
            "score": user.score
        }),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response
