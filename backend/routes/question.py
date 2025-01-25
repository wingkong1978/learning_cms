from flask import Blueprint, request, jsonify
from backend.models import Question, Exam
from backend import db

question_bp = Blueprint('question', __name__)

@question_bp.route('/questions', methods=['POST'])
def create_question():
    data = request.get_json()
    exam_id = data.get('exam_id')
    type = data.get('type')
    content = data.get('content')
    options = data.get('options')
    answer = data.get('answer')
    score = data.get('score')

    new_question = Question(exam_id=exam_id, type=type, content=content, options=options, answer=answer, score=score)
    db.session.add(new_question)
    db.session.commit()

    return jsonify({'message': 'Question created successfully'}), 201 