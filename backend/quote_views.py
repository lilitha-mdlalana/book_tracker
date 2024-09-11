
# class Quote(db.Model):
#     __tablename__ = 'quotes'
    
#     id = db.Column(db.Integer, primary_key=True)
#     content = db.Column(db.Text, nullable=False)
#     book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    
#     def to_json(self):
#         return {
#             'id': self.id,
#             'content': self.content,
#             'book_id': self.book_id
#         }

    
# # CREATE - Add a new quote to a book
# @app.route('/api/books/<int:book_id>/quotes', methods=['POST'])
# def add_quote(book_id):
#     user_id = get_jwt_identity()
#     data = request.get_json()

#     book = Book.query.filter_by(id=book_id, user_id=user_id).first()
#     if not book:
#         return jsonify({"message": "Book not found!"}), 404

#     new_quote = Quote(content=data['content'], book_id=book_id)
#     db.session.add(new_quote)
#     db.session.commit()
#     return jsonify({"message": "Quote added successfully!", "quote": new_quote.id}), 201

# # READ - Get all quotes for a book
# @app.route('/api/books/<int:book_id>/quotes', methods=['GET'])
# def get_quotes(book_id):
#     user_id = get_jwt_identity()

#     book = Book.query.filter_by(id=book_id, user_id=user_id).first()
#     if not book:
#         return jsonify({"message": "Book not found!"}), 404

#     quotes = Quote.query.filter_by(book_id=book_id).all()
#     return jsonify([{
#         'id': quote.id,
#         'content': quote.content
#     } for quote in quotes]), 200

# # UPDATE - Update a quote
# @app.route('/api/books/<int:book_id>/quotes/<int:quote_id>', methods=['PUT'])
# def update_quote(book_id, quote_id):
#     user_id = get_jwt_identity()
#     data = request.get_json()

#     book = Book.query.filter_by(id=book_id, user_id=user_id).first()
#     if not book:
#         return jsonify({"message": "Book not found!"}), 404

#     quote = Quote.query.filter_by(id=quote_id, book_id=book.id).first()
#     if not quote:
#         return jsonify({"message": "Quote not found!"}), 404

#     quote.content = data.get('content', quote.content)
#     db.session.commit()
#     return jsonify({"message": "Quote updated successfully!"}), 200

# # DELETE - Delete a quote
# @app.route('/api/books/<int:book_id>/quotes/<int:quote_id>', methods=['DELETE'])
# def delete_quote(book_id, quote_id):
#     user_id = get_jwt_identity()

#     book = Book.query.filter_by(id=book_id, user_id=user_id).first()
#     if not book:
#         return jsonify({"message": "Book not found!"}), 404

#     quote = Quote.query.filter_by(id=quote_id, book_id=book.id).first()
#     if not quote:
#         return jsonify({"message": "Quote not found!"}), 404

#     db.session.delete(quote)
#     db.session.commit()
#     return jsonify({"message": "Quote deleted successfully!"}), 200
    