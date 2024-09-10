from flask import Flask,jsonify,request
from flask_jwt_extended import JWTManager,create_access_token
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config['SECRET_KEY'] = 'ydoYQfwVsH' #! TODO: Change this to use a .env variable
app.config["JWT_SECRET_KEY"] = 'jUSkC6nojI' #! TODO: Change this to use a .env variable
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///books.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(80),nullable=False)
    is_active = db.Column(db.Boolean, default=True)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'is_active': self.is_active
        }
    


@app.route('/api/users',methods=['GET'])
def get_users():
    users = User.query.all()
    result = []
    for user in users:
        result.append({'username': user.username})
    return jsonify(result)

@app.route('/api/register',methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400
    
    hashed_password = Bcrypt.generate_password_hash(bcrypt,password=password).decode('utf-8')
    new_user = User(username=username, password=hashed_password,is_active=True)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 200


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and Bcrypt.check_password_hash(bcrypt,user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login Success', 'access_token': access_token})
    else:
        return jsonify({'message': 'Login Failed'}), 401

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)