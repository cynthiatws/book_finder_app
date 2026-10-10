from flask import Flask, render_template, request, jsonify
import requests
from book_service import search_books

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/search")
def api_search():
    query = request.args.get("q", "")
    try:
        books = search_books(query)
    except requests.RequestException:
        app.logger.exception("Book search request failed")
        return jsonify({"error": "Book search is temporarily unavailable. Please try again shortly."}), 502
    return jsonify({"books": books})

if __name__ == "__main__":
    app.run(debug=True, port=5000)