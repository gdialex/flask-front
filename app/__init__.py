from flask import Flask

app = Flask(__name__)

USERS = []  # list for objects of type User
EXPRS = []  # list for objects of type Expression
QUEST = []  # list of questions

from app import views_all
from app import models
from app import views
