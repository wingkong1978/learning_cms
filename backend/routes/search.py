from flask import Blueprint, request, jsonify
from backend.models.question import Question

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search_questions():
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({
            'results': [],
            'total': 0
        })

    questions = Question.query.filter(Question.content.like(f'%{keyword}%')).all()
    results = [q.to_dict() for q in questions]
    
    return jsonify({
        'results': results,
        'total': len(results)
    }) 