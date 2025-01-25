from flask import Blueprint, request, jsonify
from backend.models import Exam, User
from backend import db

exam_bp = Blueprint('exam', __name__)

@exam_bp.route('/exams', methods=['POST'])
def create_exam():
    data = request.get_json()
    title = data.get('title')
    subject = data.get('subject')
    difficulty = data.get('difficulty')
    created_by = data.get('created_by')

    new_exam = Exam(title=title, subject=subject, difficulty=difficulty, created_by=created_by)
    db.session.add(new_exam)
    db.session.commit()

    return jsonify({'message': 'Exam created successfully'}), 201

@exam_bp.route('/exams', methods=['GET'])
def get_exams():
    exams = Exam.query.all()
    return jsonify([{'id': exam.id, 'title': exam.title, 'subject': exam.subject} for exam in exams]), 200 