from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from backend.config import Config
from backend.extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    Migrate(app, db)

    # 注册蓝图
    from backend.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app 