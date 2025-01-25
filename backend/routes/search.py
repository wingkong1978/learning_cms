from flask import Blueprint, request, jsonify
from backend.models import Question

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search_questions():
    keyword = request.args.get('keyword')
    questions = Question.query.filter(Question.content.like(f'%{keyword}%')).all()
    return jsonify([{'id': q.id, 'content': q.content} for q in questions]), 200 