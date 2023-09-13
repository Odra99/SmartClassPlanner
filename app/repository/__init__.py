from app.repository import teacher_repository
from app.repository import class_repository
from app.repository import course_repository
from app.repository import general_repository
from app.repository import schedule_repository

from flask import Blueprint

bp = Blueprint('repository',__name__)

from app.repository import routes