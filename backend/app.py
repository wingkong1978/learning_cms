import os
import sys

# 将项目根目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify
from flask_migrate import Migrate
from backend.config import Config
from backend.extensions import db  # 从 extensions.py 导入 db

app = Flask(__name__)
app.config.from_object(Config)

# 初始化 db
db.init_app(app)
migrate = Migrate(app, db)

# 添加根路径路由
@app.route('/')
def index():
    return jsonify({'message': 'Hello from the backend!'})

# 注册路由
from backend.routes.auth import auth_bp
from backend.routes.exam import exam_bp
from backend.routes.question import question_bp
from backend.routes.search import search_bp

app.register_blueprint(auth_bp)
app.register_blueprint(exam_bp)
app.register_blueprint(question_bp)
app.register_blueprint(search_bp)

if __name__ == '__main__':
    app.run(debug=True) 