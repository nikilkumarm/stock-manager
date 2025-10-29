from flask import Flask, request, jsonify, abort
import sqlite3

app = Flask(__name__)
DB_PATH = "stock.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        qty INTEGER NOT NULL
    );
    """)
    conn.close()

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/items", methods=["GET"])
def get_items():
    conn = sqlite3.connect(DB_PATH)
    items = conn.execute("SELECT id, name, qty FROM items").fetchall()
    conn.close()
    return jsonify([{"id": i[0], "name": i[1], "qty": i[2]} for i in items])

@app.route("/api/items", methods=["POST"])
def add_item():
    data = request.get_json()
    if not data or "name" not in data or "qty" not in data:
        abort(400)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO items (name, qty) VALUES (?, ?)", (data["name"], data["qty"]))
    conn.commit()
    conn.close()
    return jsonify({"status": "created"}), 201

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5050)
