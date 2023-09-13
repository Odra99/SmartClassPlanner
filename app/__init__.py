from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from config import Config
from app.extensions import db,ma
from app.model import *
from app.ETL import *
from app.main.schedule import *

def create_app(config_class=Config):

    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app,db)    

    from app.main import bp as main_bp
    from app.ETL import bp as etl_bp
    from app.repository import bp as repository_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(etl_bp)
    app.register_blueprint(repository_bp)

    @app.get("/hello")
    def home():
        schedule.scheduleGeneration()
        return "Hello, world!!"
    
    return app




