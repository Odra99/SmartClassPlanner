from flask import Flask
from flask_migrate import Migrate

from config import Config
from app.extensions import db
from app.model import *
from app.ETL import *


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate = Migrate(app,db)    

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    @app.get("/hello")
    def home():
        generalETL.etlArea('/home/odra/Documents/Area.csv')
        return "Hello, world!!"
    
    return app




