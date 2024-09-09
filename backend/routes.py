from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask import jsonify, request

from main import db
from models import User

@app.route('/register',methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400
    
    hashed_password = Bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 200


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and Bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login Success', 'access_token': access_token})
    else:
        return jsonify({'message': 'Login Failed'}), 401

