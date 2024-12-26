import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ініціалізація бази
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            icon_url TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    icon_url = data.get("icon_url", "default-icon.png")

    if not username or not password:
        return jsonify({"message": "Username and password required"}), 400

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, icon_url) VALUES (?, ?, ?)",
                   (username, password, icon_url))
    conn.commit()
    conn.close()

    return jsonify({"message": "User registered successfully"}), 201

@app.route("/api/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username, icon_url FROM users")
    users = cursor.fetchall()
    conn.close()

    return jsonify([
        {"username": row[0], "icon_url": row[1]} for row in users
    ])

if __name__ == "__main__":
    app.run(debug=True)
