from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Static array of books
books = [
    {"id": 1, "title": "The Pragmatic Programmer", "author": "Andy Hunt & Dave Thomas"},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin"},
    {"id": 3, "title": "Introduction to Algorithms", "author": "Thomas H. Cormen"},
    {"id": 4, "title": "The Phoenix Project", "author": "Gene Kim"},
    {"id": 5, "title": "Designing Data-Intensive Applications", "author": "Martin Kleppmann"},
    {"id": 6, "title": "Artificial Intelligence: A Guide for Thinking Humans", "author": "Melanie Mitchell"},
]

@app.route("/")
def hello():
    return "Add the correct route, for example /random-book"

@app.route('/random-book', methods=['GET'])
def get_random_book():
    """Returns a random book from the static list"""
    random_book = random.choice(books)  # Select a random book
    #convert string to  object
    #json_object = json.loads(random_book)
    return jsonify({"message": "Book retrieved successfully", "book": random_book}), 200

@app.route('/update-book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Updates book details based on the given book ID"""
    data = request.json  # Get request data
    for book in books:
        if book["id"] == book_id:
            book.update(data)  # Update book with new data
            return jsonify({"message": "Book updated successfully", "book": book}), 200
    return jsonify({"error": "Book not found"}), 404

@app.route('/delete-book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Deletes a book by its ID"""
    global books
    books = [book for book in books if book["id"] != book_id]  # Remove book
    return jsonify({"message": f"Book with ID {book_id} deleted successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
