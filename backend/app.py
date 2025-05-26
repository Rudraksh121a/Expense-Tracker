from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = "expenses.db"

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/add-expense", methods=["POST"])
def add_expense():
    data = request.json
    if not data or "amount" not in data or "category" not in data or "date" not in data:
        return jsonify({"error": "Invalid data"}), 400

    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO expenses (amount, category, date) VALUES (?, ?, ?)",
        (data["amount"], data["category"], data["date"])
    )
    expense_id = c.lastrowid
    conn.commit()
    conn.close()
    return jsonify({"message": "Expense added successfully", "id": expense_id}), 201

@app.route("/get-expenses", methods=["GET"])
def get_expenses():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM expenses")
    expenses = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(expenses), 200

@app.route("/remove-expense/<int:expense_id>", methods=["DELETE"])
def remove_expense(expense_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    if c.rowcount == 0:
        conn.close()
        return jsonify({"error": "Expense not found"}), 404
    conn.commit()
    conn.close()
    return jsonify({"message": "Expense removed successfully"}), 200

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
