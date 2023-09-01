from app import app, USERS, EXPRS, models
from flask import request, Response
import json
from http import HTTPStatus
import random
import re


@app.route("/")
def index():
    return "<h1>Hello world</h1>"


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
    if user_id < 0 or user_id >= len(USERS):
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


@app.get("/math/expression")
def generate_expr():
    data = request.get_json()
    expr_id = len(EXPRS)
    count_nums = data["count_nums"]
    operation = data["operation"]  # expect +,*,-,//,**,
    if operation == "random":
        operation = random.choice(["+", "*", "-", "//", "**"])
    min_num = data["min"]
    max_num = data["max"]

    if count_nums <= 1 or (count_nums > 2 and operation not in {"+", "*"}):
        return Response(status=HTTPStatus.BAD_REQUEST)

    values = [random.randint(min_num, max_num) for _ in range(count_nums)]
    expression = models.Expression(expr_id, operation, *values)
    EXPRS.append(expression)

    response = Response(
        json.dumps(
            {
                "id": expression.id,
                "operation": expression.operation,
                "values": expression.values,
                "string_expression": expression.to_string(),
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response


@app.get("/math/<int:expr_id>")
def get_expr(expr_id):

    if expr_id < 0 or expr_id >= len(EXPRS):
        return Response(status=HTTPStatus.NOT_FOUND)
    expression = EXPRS[expr_id]

    response = Response(
        json.dumps(
            {
                "id": expression.id,
                "operation": expression.operation,
                "values": expression.values,
                "string_expression": expression.to_string(),
            }
        ),
        HTTPStatus.OK,
        mimetype="application/json",
    )
    return response
