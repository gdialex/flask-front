from app import app, USERS, QUEST, models
from flask import request, Response, url_for
import json
from http import HTTPStatus
import random


@app.post("/questions/create")
def create_question():
    data = request.get_json()
    title = data["title"]
    description = data["description"]
    question_type = data["type"]
    question_id = len(QUEST)
    question = None
    if question_type == "ONE-ANSWER":
        answer = data["answer"]  # expect string
        if not models.OneAnswer.is_valid(answer):
            return Response("answer must be string", status=HTTPStatus.BAD_REQUEST)
        question = models.OneAnswer(question_id, title, description, answer, reward=1)
    elif question_type == "MULTIPLE-CHOICE":
        choices = data["choices"]  # list of choices
        answer = data["answer"]  # expect number
        if not models.MultipleChoice.is_valid(answer, choices):
            return Response(
                "answer must be int, choices must be list. 0<=answer<=len(choices)",
                status=HTTPStatus.BAD_REQUEST,
            )
        question = models.MultipleChoice(
            question_id, title, description, answer, choices, reward=1
        )
    if question is None:
        return Response(
            "Question must be of ONE-ANSWER or MULTIPLE-CHOICE type",
            status=HTTPStatus.BAD_REQUEST,
        )
    QUEST.append(question)
    return Response(
        json.dumps(
            {
                "id": question.id,
                "title": question.title,
                "description": question.description,
                "type": question_type,
                "answer": question.answer,
            }
        ),
        status=HTTPStatus.CREATED,
        mimetype="application/json",
    )


@app.get("/questions/random")
def get_random_question():
    if len(QUEST) == 0:
        return Response(
            f'No questions in the database. Please, <a href="{url_for("create_question")}">add some questions first</a>',
            status=HTTPStatus.NOT_FOUND,
        )
    question_id = random.randint(0, len(QUEST) - 1)
    question = QUEST[question_id]
    return Response(
        json.dumps(
            {
                "id": question.id,
                "reward": question.reward,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )


@app.post("/questions/<int:question_id>/solve")
def solve_question(question_id):
    data = request.get_json()
    user_id = data["user_id"]
    user_answer = data["user_answer"]
    if not models.User.is_valid_id(user_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    if not models.Question.is_valid_id(question_id):
        return Response(status=HTTPStatus.NOT_FOUND)
    question = QUEST[question_id]
    user = USERS[user_id]
    if isinstance(question, models.MultipleChoice):
        if not isinstance(user_answer, int):
            return Response(
                "Это вопрос с множественным выбором, пожалуйста, введите число",
                status=HTTPStatus.BAD_REQUEST,
            )
    if isinstance(question, models.OneAnswer):
        if not isinstance(user_answer, str):
            return Response(
                "Это вопрос с одним ответом, пожалуйста, введите строку",
                status=HTTPStatus.BAD_REQUEST,
            )

    if user_answer == question.answer:
        user.increase_score(question.reward)
        result = "Correct"
        reward = question.reward
    else:
        result = "Wrong"
        reward = 0

    user.solve(question, user_answer)  # add to history

    return Response(
        json.dumps(
            {
                "question_id": question.id,
                "result": result,
                "reward": reward,
            }
        ),
        status=HTTPStatus.OK,
        mimetype="application/json",
    )
