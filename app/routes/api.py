import sys
from flask import Blueprint, request, jsonify, session
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
        print(sys.exc_info()[0])

        # insert failed, so rollback and send error to front end
        db.rollback()
        return jsonify(message = 'Signup failed'), 500

@bp.route('/users/logout', methods=['POST'])
def logout():
    # remove session variables
    session.clear()
    return '', 204

@bp.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()
    db = get_db()

    try:
        # query user by email
        user = db.query(User).filter(User.email == data['email']).one()

        # check if password is correct
        if user.verify_password(data['password']) == False:
            return jsonify(message = 'Incorrect credentials'), 400
        
        session.clear()
        session['user_id'] = user.id
        session['loggedIn'] = True
        return jsonify(id = user.id)
    
    except:
        print(sys.exc_info()[0])
        
    # you can create sessions in Flask only if you've defined a secret key. Fortunately, the following code in app/__init__.py does just that: app.config.from_mapping(SECRET_KEY='super_secret_key'). In a production environment, you should change this key to something that's harder to guess.
    session.clear()
    session['user_id'] = user.id
    session['loggedIn'] = True
    
    return jsonify(id = user.id)