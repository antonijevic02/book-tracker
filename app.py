from flask import Flask, jsonify, request, abort
from models import Base, engine, SessionLocal, Book

app = Flask(__name__)

# In-memory data for now (later we’ll connect to Azure SQL)
books = []

Base.metadata.create_all(bind=engine)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/books", methods=["GET"])
def get_books():
    session = SessionLocal()
    books = session.query(Book).all()
    session.close()
    return jsonify([{"id": b.id, "title": b.title, "author": b.author} for b in books])

@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()
    if not data or "title" not in data:
        abort(400, "Missing title")
    book = Book(title=data["title"], author=data.get("author", ""))
    session = SessionLocal()
    session.add(book)
    session.commit()
    session.refresh(book)
    session.close()
    return jsonify({"id": book.id, "title": book.title, "author": book.author}), 201

@app.route("/books/<int:id>", methods=["PUT"])
def update_book(id):
    data = request.get_json()
    session = SessionLocal()
    book = session.query(Book).get(id)
    if not book:
        session.close()
        abort(404)
    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    session.commit()
    session.refresh(book)
    session.close()
    return jsonify({"id": book.id, "title": book.title, "author": book.author})

@app.route("/books/<int:id>", methods=["DELETE"])
def delete_book(id):
    session = SessionLocal()
    book = session.query(Book).get(id)
    if not book:
        session.close()
        abort(404)
    session.delete(book)
    session.commit()
    session.close()
    return jsonify({"message": "Deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
