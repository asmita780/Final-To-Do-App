from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def creat_app():

    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'MY_SECRET_KEY'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

    db.__init__(app)

    from app.modules import Task

    with app.app_context():
        
        db.create_all()


    from app.routes.auths import auth_bp
    from app.routes.tasks import task_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app

    