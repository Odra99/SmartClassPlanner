from app.ETL import generalETL
from app.ETL import teacherETL
from flask import Blueprint

bp = Blueprint('etl',__name__)

from app.ETL import routes