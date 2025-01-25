from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# 注册路由
from routes.auth import auth_bp
from routes.exam import exam_bp
from routes.question import question_bp
from routes.search import search_bp

app.register_blueprint(auth_bp)
app.register_blueprint(exam_bp)
app.register_blueprint(question_bp)
app.register_blueprint(search_bp)

if __name__ == '__main__':
    app.run(debug=True) 