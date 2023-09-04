from app import app, USERS, models
from flask import request, Response
import json
from http import HTTPStatus


@app.post("/user/create")
def user_create():
    data = request.get_json()
    user_id = len(USERS)
    first_name = data["first_name"]
    last_name = data["last_name"]
    phone = data["phone"]
    email = data["email"]

    if not models.User.is_valid_email(email) or not models.User.is_valid_phone(phone):
        return Response(status=HTTPStatus.BAD_REQUEST)
    user = models.User(user_id, first_name, last_name, phone, email)

    USERS.append(user)
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "score": user.score,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/user/<int:user_id>")
def get_user(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    user = USERS[user_id]
    response = Response(
        json.dumps(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "email": user.email,
                "score": user.score,
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/users/<int:user_id>/history")
def get_user_history(user_id):
    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.NOT_FOUND)

    user = USERS[user_id]
    return Response(
        json.dumps({"history": user.history}),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
