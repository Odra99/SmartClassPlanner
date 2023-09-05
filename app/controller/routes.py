from app.controller import bp


@bp.route('/')
def index():
    return 'This is the main blueprint'