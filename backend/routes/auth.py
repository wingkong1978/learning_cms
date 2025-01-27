from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from backend.models.user import User
from backend.extensions import db
from backend.config import Config
import re
import jwt
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

def validate_password(password):
    """验证密码强度"""
    if len(password) < 8:
        return False, "密码长度至少8个字符"
    if not re.search(r"[A-Za-z]", password):
        return False, "密码必须包含字母"
    if not re.search(r"\d", password):
        return False, "密码必须包含数字"
    if not re.search(r"[!@#$%^&*]", password):
        return False, "密码必须包含特殊字符"
    return True, None

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # 验证必填字段
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if not data.get(field):
            return jsonify({
                'error': 'ValidationError',
                'message': f'{field} 是必填项'
            }), 400

    username = data['username']
    email = data['email']
    password = data['password']

    # 验证用户名格式
    if not re.match(r'^[a-zA-Z0-9_]{3,50}$', username):
        return jsonify({
            'error': 'ValidationError',
            'message': '用户名只能包含字母、数字和下划线，长度3-50个字符'
        }), 400

    # 验证邮箱格式
    if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', email):
        return jsonify({
            'error': 'ValidationError',
            'message': '请输入有效的邮箱地址'
        }), 400

    # 验证密码强度
    is_valid, error_message = validate_password(password)
    if not is_valid:
        return jsonify({
            'error': 'ValidationError',
            'message': error_message
        }), 400

    # 检查用户名是否已存在
    if User.query.filter_by(username=username).first():
        return jsonify({
            'error': 'DuplicateError',
            'message': '用户名已被使用'
        }), 400

    # 检查邮箱是否已注册
    if User.query.filter_by(email=email).first():
        return jsonify({
            'error': 'DuplicateError',
            'message': '该邮箱已被注册'
        }), 400

    try:
        # 创建新用户
        user = User(
            username=username,
            email=email,
            password=password
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({
            'message': '注册成功',
            'userId': user.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'ServerError',
            'message': '注册失败，请稍后重试'
        }), 500

@auth_bp.route('/check-username', methods=['GET'])
def check_username():
    username = request.args.get('username')
    if not username:
        return jsonify({
            'error': 'ValidationError',
            'message': '用户名是必填项'
        }), 400

    user = User.query.filter_by(username=username).first()
    return jsonify({
        'available': user is None
    })

@auth_bp.route('/check-email', methods=['GET'])
def check_email():
    email = request.args.get('email')
    if not email:
        return jsonify({
            'error': 'ValidationError',
            'message': '邮箱是必填项'
        }), 400

    user = User.query.filter_by(email=email).first()
    return jsonify({
        'available': user is None
    })

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return jsonify({
            'message': 'Please login with POST request',
            'required_fields': ['username', 'password']
        })

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401

    token = jwt.encode(
        {
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        },
        Config.JWT_SECRET_KEY,
        algorithm='HS256'
    )

    return jsonify({
        'token': token,
        'user': user.to_dict()
    }), 200 