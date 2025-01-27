import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, redirect, url_for
from flask_migrate import Migrate
from backend.config import Config
from backend.extensions import db
from backend.routes.auth import auth_bp
from backend.routes.search import search_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    db.init_app(app)
    Migrate(app, db)

    # 注册蓝图
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(search_bp, url_prefix='/api')

    # 根路由重定向
    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    # 404错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested URL was not found on the server.'
        }), 404

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 