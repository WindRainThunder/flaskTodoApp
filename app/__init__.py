from flask_sqlalchemy import SQLAlchemy
import os
from flask import Flask
from app.extensions import db

def create_app():
    app = Flask(__name__)

    base_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = os.path.dirname(base_dir)
    db_path = os.path.join(project_root, "app", "databases", "todo.db") 
    app.config["SECRET_KEY"] = "secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes import bp
    app.register_blueprint(bp)
    

    with app.app_context():
        from app.startup import clear_test_user_tasks
        clear_test_user_tasks()

    return app