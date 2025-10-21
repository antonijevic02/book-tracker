from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# In-memory data for now (later we’ll connect to Azure SQL)
books = []

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)

@app.route("/books", methods=["POST"])
def add_book():
    data = request.get_json()
    if not data or "title" not in data:
        abort(400, "Missing title")
    book = {
        "id": len(books) + 1,
        "title": data["title"],
        "author": data.get("author", ""),
    }
    books.append(book)
    return jsonify(book), 201

if __name__ == "__main__":
    app.run(debug=True)
