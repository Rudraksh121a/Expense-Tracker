from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

expenses = []

@app.route("/add-expense", methods=["POST"])
def add_expense():
    data = request.json
    if not data or "amount" not in data or "category" not in data or "date" not in data:
        return jsonify({"error": "Invalid data"}), 400

    expenses.append(data)
    return jsonify({"message": "Expense added successfully"}), 201

@app.route("/get-expenses", methods=["GET"])
def get_expenses():
    return jsonify(expenses), 200

if __name__ == "__main__":
    # Run on all interfaces so device/emulator can reach it on your network IP
    app.run(host="0.0.0.0", port=5000, debug=True)
