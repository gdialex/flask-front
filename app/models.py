# models.py
import re
from app import USERS, EXPRS, QUEST
from abc import ABC, abstractmethod


class User:
    def __init__(self, id, first_name, last_name, phone, email, score=0):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.score = score
        self.history = []
        self.status = "created"

    @staticmethod
    def is_valid_email(email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        return False

    @staticmethod
    def is_valid_phone(phone):
        if re.match(r"^\+?[1-9][0-9]{7,14}$", phone):
            return True
        return False

    @staticmethod
    def is_valid_id(user_id):
        return 0 <= user_id < len(USERS) and USERS[user_id].status != "deleted"

    def increase_score(self, amount=1):
        self.score += amount

    def repr(self):
        if self.status == "created":
            return f"{self.id}) {self.first_name} {self.last_name}"
        else:
            return "DELETED"

    def solve(self, task, user_answer):
        if not isinstance(task, Question) and not isinstance(task, Expression):
            return
        result = task.to_dict()
        result["user_answer"] = user_answer
        result["reward"] = task.reward if user_answer == task.answer else 0
        self.history.append(result)

    def __lt__(self, other):
        return self.score < other.score

    def to_dict(self):
        return dict(
            {
                "id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "score": self.score,
            }
        )

    @staticmethod
    def get_leaderboard():
        return [
            user.to_dict()
            for user in sorted(USERS, reverse=True)
            if User.is_valid_id(user.id)
        ]


class Expression:
    def __init__(self, id, operation, *values, reward=None):
        self.id = id
        self.operation = operation
        self.values = values
        self.answer = self.__evaluate()
        if reward is None:
            reward = len(values) - 1
        self.reward = reward
        self.status = "created"

    def __evaluate(self):
        return eval(self.to_string())

    def to_string(self):
        expr_str = str(self.values[0]) + "".join(
            f" {self.operation} {value}" for value in self.values[1:]
        )
        return expr_str

    @staticmethod
    def is_valid_id(expr_id):
        return 0 <= expr_id < len(EXPRS) and EXPRS[expr_id].status != "deleted"

    def repr(self):
        if self.status == "created":
            return f"{self.id}) {self.to_string()} = {self.answer}"
        else:
            return "DELETED"

    def to_dict(self):
        return dict(
            {
                "id": self.id,
                "operation": self.operation,
                "values": self.values,
                "string_expression": self.to_string(),
            }
        )


class Question(ABC):
    def __init__(self, id, title, description, reward=None):
        self.id = id
        self.title = title
        self.description = description
        if reward is None:
            reward = 1
        self.reward = reward
        self.status = "created"

    @property
    @abstractmethod
    def answer(self):
        pass

    @property
    @abstractmethod
    def type(self):
        pass

    def repr(self):
        if self.status == "created":
            return f"{self.id}) {self.title}"
        else:
            return "DELETED"

    @staticmethod
    def is_valid_id(question_id):
        return 0 <= question_id < len(QUEST) and QUEST[question_id].status != "deleted"


class OneAnswer(Question):
    def __init__(self, id, title, description, answer: str, reward=None):
        super().__init__(id, title, description, reward)
        if self.is_valid(answer):
            self._answer = answer
        else:
            self._answer = None

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, value: str):
        if self.is_valid(value):
            self._answer = value

    @property
    def type(self):
        return "ONE-ANSWER"

    @staticmethod
    def is_valid(answer):
        return isinstance(answer, str)

    def to_dict(self):
        return dict(
            {
                "title": self.title,
                "description": self.description,
                "type": "ONE-ANSWER",
            }
        )


class MultipleChoice(Question):
    def __init__(self, id, title, description, answer: int, choices: list, reward=None):
        super().__init__(id, title, description, reward)
        if self.is_valid(answer, choices):
            self.choices = choices
            self._answer = answer
        else:
            self.choices = None
            self._answer = None

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, value: int):
        if self.is_valid(value, self.choices):
            self._answer = value

    @property
    def type(self):
        return "MULTIPLE-CHOICE"

    @staticmethod
    def is_valid(answer, choices):
        if not isinstance(answer, int) or not isinstance(choices, list):
            return False
        if answer < 0 or answer >= len(choices):
            return False
        return True

    def to_dict(self):
        return dict(
            {
                "title": self.title,
                "description": self.description,
                "type": "MULTIPLE-CHOICE",
                "choices": self.choices,
            }
        )
