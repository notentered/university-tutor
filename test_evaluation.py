from flask import Blueprint, jsonify, request
from db_models import Question, Option, engine
from sqlalchemy.orm import Session

test_evaluation_blueprint = Blueprint('test_evaluation', __name__)


@test_evaluation_blueprint.route('/evaluate', methods=['POST'])
def evaluate_test():
    user_answers = request.json.get(
        'answers')  # assuming the format {"answers": [{"question_id": "..", "option_id": ".."}, ...]}

    with Session(engine) as session:
        incorrect_answers = []

        for answer in user_answers:
            question = session.query(Question).get(answer['question_id'])
            selected_option = session.query(Option).get(answer['option_id'])

            if not selected_option.is_correct:
                incorrect_answers.append({
                    "question_id": question.id,
                    "question_title": question.title,
                    "answer_description": question.answer_description
                })

    return jsonify({"incorrect_answers": incorrect_answers})