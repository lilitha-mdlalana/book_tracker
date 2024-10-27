from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

app.config['SECRET_KEY'] = 'ydoYQfwVsH'
app.config["JWT_SECRET_KEY"] = 'jUSkC6nojI'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Quote(db.Model):
    __tablename__ = 'quotes'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)

# Register route
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, password=hashed_password, is_active=True)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 200

# Login route
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login Success', 'access_token': access_token})
    else:
        return jsonify({'message': 'Login Failed'}), 401

# CREATE - Add a new book
@app.route('/api/books', methods=['POST'])
@jwt_required()
def add_book():
    user_id = get_jwt_identity()
    data = request.get_json()

    new_book = Book(
        title=data['title'],
        author=data['author'],
        description=data.get('description', ''),
        image_url=data.get('image_url', ''),
        genre=data.get('genre', ''),
        total_pages=data['total_pages'],
        current_page=data.get('current_page', 0),
        completed=data.get('completed', False),
        user_id=user_id
    )
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added successfully!", "book": new_book.id}), 201

# READ - Get all books for the logged-in user
@app.route('/api/books', methods=['GET'])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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
@jwt_required()
def delete_book(book_id):
    user_id = get_jwt_identity()

    book = Book.query.filter_by(id=book_id, user_id=user_id).first()
    if not book:
        return jsonify({"message": "Book not found!"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully!"}), 200

# CREATE - Add a new quote to a book
@app.route('/api/books/<int:book_id>/quotes', methods=['POST'])
@jwt_required()
def add_quote(book_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    book = Book.query.filter_by(id=book_id, user_id=user_id).first()
    if not book:
        return jsonify({"message": "Book not found!"}), 404

    new_quote = Quote(content=data['content'], book_id=book_id)
    db.session.add(new_quote)
    db.session.commit()
    return jsonify({"message": "Quote added successfully!", "quote": new_quote.id}), 201

# READ - Get all quotes for a book
@app.route('/api/books/<int:book_id>/quotes', methods=['GET'])
@jwt_required()
def get_quotes(book_id):
    user_id = get_jwt_identity()

    book = Book.query.filter_by(id=book_id, user_id=user_id).first()
    if not book:
        return jsonify({"message": "Book not found!"}), 404

    quotes = Quote.query.filter_by(book_id=book_id).all()
    return jsonify([{
        'id': quote.id,
        'content': quote.content
    } for quote in quotes]), 200

# UPDATE - Update a quote
@app.route('/api/books/<int:book_id>/quotes/<int:quote_id>', methods=['PUT'])
@jwt_required()
def update_quote(book_id, quote_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    book = Book.query.filter_by(id=book_id, user_id=user_id).first()
    if not book:
        return jsonify({"message": "Book not found!"}), 404

    quote = Quote.query.filter_by(id=quote_id, book_id=book.id).first()
    if not quote:
        return jsonify({"message": "Quote not found!"}), 404

    quote.content = data.get('content', quote.content)
    db.session.commit()
    return jsonify({"message": "Quote updated successfully!"}), 200

# DELETE - Delete a quote
@app.route('/api/books/<int:book_id>/quotes/<int:quote_id>', methods=['DELETE'])
@jwt_required()
def delete_quote(book_id, quote_id):
    user_id = get_jwt_identity()

    book = Book.query.filter_by(id=book_id, user_id=user_id).first()
    if not book:
        return jsonify({"message": "Book not found!"}), 404

    quote = Quote.query.filter_by(id=quote_id, book_id=book.id).first()
    if not quote:
        return jsonify({"message": "Quote not found!"}), 404

    db.session.delete(quote)
    db.session.commit()
    return jsonify({"message": "Quote deleted successfully!"}), 200

with app.app_context():
    db.create_all()
    
    
if __name__ == '__main__':
    print('databases created successfully');
    app.run(debug=True)
