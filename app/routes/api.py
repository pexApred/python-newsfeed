import sys
from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')
# connect to the database (.routes)
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


@bp.route('/comments', methods=['POST'])
def comment():
    # Create a new model instance using the request data.
    data = request.get_json()
    db = get_db()
    # Try to save the instance using a try...except statement.
    try:
        # create a new comment
        newComment = Comment(
            comment_text = data['comment_text'],
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )

        # save in database
        db.add(newComment)
        db.commit()
    except:
        print(sys.exc_info()[0])
        # Rollback the session if an error occurred and return a 500 status code.
        db.rollback()
        # Return a status of 500 if it failed or the new ID if it succeeded.
        return jsonify(message = 'Comment failed'), 500
    
    return jsonify(id = newComment.id)

@bp.route('/posts', methods=['POST'])
def create():
    data = request.get_json()
    db = get_db()

    try:
        # create new post
        newPost = Post(
            title = data['title'],
            post_url = data['post_url'],
            user_id = session.get('user_id')
        )

        db.add(newPost)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Post failed'), 500
    
    return jsonify(id = newPost.id)

@bp.route('/posts/upvote', methods=['PUT'])
def upvote():
    data = request.get_json()
    db = get_db()

    try:
        # create a new vote with incoming id and session id
        newVote = Vote(
            post_id = data['post_id'],
            user_id = session.get('user_id')
        )

        db.add(newVote)
        db.commit()
    except:
        print(sys.exc_info()[0])

        db.rollback()
        return jsonify(message = 'Upvote failed'), 500
    
    return '', 204

