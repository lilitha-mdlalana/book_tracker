from flask import Flask,jsonify,request
from flask_jwt_extended import JWTManager,create_access_token,get_jwt_identity, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config['SECRET_KEY'] = 'ydoYQfwVsH' 
app.config["JWT_SECRET_KEY"] = 'jUSkC6nojI' 
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///books.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

#! Models
class User(db.Model):
    __table_name__ = 'users'
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

class Book(db.Model):
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)  
    title = db.Column(db.String(255), nullable=False)  
    author = db.Column(db.String(255), nullable=False)  
    description = db.Column(db.Text, nullable=True)  
    image_url = db.Column(db.String(255), nullable=True)  
    genre = db.Column(db.String(100), nullable=True)  
    total_pages = db.Column(db.Integer, nullable=False)  
    current_page = db.Column(db.Integer, nullable=False)  
    completed = db.Column(db.Boolean, default=False)  
    quotes = db.relationship('Quote', backref='book', lazy=True)  

    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'image_url': self.image_url,
            'genre': self.genre,
            'total_pages': self.total_pages,
            'current_page': self.current_page,
            'completed': self.completed,
            'user_id': self.user_id
        }


#! Views
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
    print(username,password)

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

# READ - Get all books for the logged-in user
@app.route('/api/books', methods=['GET'])
def get_books():
    user_id = get_jwt_identity()
    books = Book.query.filter_by(user_id=user_id).all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'image_url': book.image_url,
        'genre': book.genre,
        'total_pages': book.total_pages,
        'current_page': book.current_page,
        'completed': book.completed
    } for book in books]), 200

# READ - Get a single book by its ID
@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    user_id = get_jwt_identity()
    book = Book.query.filter_by(id=book_id, user_id=user_id).first()
    if not book:
        return jsonify({"message": "Book not found!"}), 404

    return jsonify({
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'description': book.description,
        'image_url': book.image_url,
        'genre': book.genre,
        'total_pages': book.total_pages,
        'current_page': book.current_page,
        'completed': book.completed
    }), 200

# UPDATE - Update a book's details
@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    book = Book.query.filter_by(id=book_id, user_id=user_id).first()
    if not book:
        return jsonify({"message": "Book not found!"}), 404

    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    book.description = data.get('description', book.description)
    book.image_url = data.get('image_url', book.image_url)
    book.genre = data.get('genre', book.genre)
    book.total_pages = data.get('total_pages', book.total_pages)
    book.current_page = data.get('current_page', book.current_page)
    book.completed = data.get('completed', book.completed)

    db.session.commit()
    return jsonify({"message": "Book updated successfully!"}), 200

# DELETE - Delete a book
@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    user_id = get_jwt_identity()

    book = Book.query.filter_by(id=book_id, user_id=user_id).first()
    if not book:
        return jsonify({"message": "Book not found!"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully!"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)