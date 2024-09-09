from flask import Flask,jsonify,request

from flask_alchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_strong_secret_key'
app.config["JWT_SECRET_KEY"] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///books.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)