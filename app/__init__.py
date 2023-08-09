from flask import Flask
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    from app.routes import bp as main_bp
    app.register_blueprint(main_bp)


    return app

app = create_app()  # Esto debe estar fuera de la función
