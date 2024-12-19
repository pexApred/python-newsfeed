import sys
from flask import Blueprint, request, jsonify
from app.models import User
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
    data = request.get_json()
    db = get_db()
    try:
        # attempt at creating a new user
        newUser = User(
            username = data['username'],
            email = data['email'],
            password = data['password']
        )

        # save in database
        db.add(newUser)
        db.commit()
    except:
        print(sys.exe_info()[0])

        # insert failed, so rollback and send error to front end
        db.rollback()
        return jsonify(message = 'Signup failed'), 500

    return jsonify(id = newUser.id)