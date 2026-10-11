from flask import Flask, request, jsonify, send_from_directory
import os
import db

# Initialize Flask app
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))
app = Flask(__name__, static_folder=FRONTEND_DIR)


# Enable Cross-Origin Resource Sharing (CORS) manually
@app.after_request
def enable_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


# Route to serve frontend homepage if opened directly at http://127.0.0.1:5000
@app.route("/")
def serve_index():
    return send_from_directory(FRONTEND_DIR, "index.html")


# Route to serve CSS and JS static assets
@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)


# ---------------- API ENDPOINTS (COLD STORAGE) ---------------- #

# 1. READ: GET all items in cold storage
@app.route("/api/items", methods=["GET"])
def get_items():
    """Returns a list of all cold storage items currently in the database."""
    items = db.get_all_items()
    return jsonify({"success": True, "data": items}), 200


# 2. CREATE: POST a new item into cold storage
@app.route("/api/items", methods=["POST"])
def create_item():
    """Adds a new item to cold storage."""
    data = request.get_json(silent=True) or {}
    item_id = data.get("item_id", "").strip()
    item_name = data.get("item_name", "").strip()
    category = data.get("category", "").strip()
    temperature = data.get("temperature", "").strip()

    # Input validation
    if not item_id or not item_name or not category or not temperature:
        return jsonify({
            "success": False,
            "message": "All fields (Item ID, Name, Category, Temperature) are required."
        }), 400

    success, message = db.add_item(item_id, item_name, category, temperature)
    status_code = 201 if success else 400
    return jsonify({"success": success, "message": message}), status_code


# 3. UPDATE: PUT updated details for an existing item
@app.route("/api/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    """Updates an existing item's name, category, and temperature."""
    data = request.get_json(silent=True) or {}
    item_name = data.get("item_name", "").strip()
    category = data.get("category", "").strip()
    temperature = data.get("temperature", "").strip()

    if not item_name or not category or not temperature:
        return jsonify({
            "success": False,
            "message": "Name, Category, and Temperature are required for update."
        }), 400

    success, message = db.update_item(item_id, item_name, category, temperature)
    status_code = 200 if success else 404
    return jsonify({"success": success, "message": message}), status_code


# 4. DELETE: DELETE an item from cold storage
@app.route("/api/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    """Deletes an item record by Item ID."""
    success, message = db.delete_item(item_id)
    status_code = 200 if success else 404
    return jsonify({"success": success, "message": message}), status_code


# Handle OPTIONS preflight requests
@app.route("/api/items", methods=["OPTIONS"])
@app.route("/api/items/<item_id>", methods=["OPTIONS"])
def handle_options(item_id=None):
    return "", 200


if __name__ == "__main__":
    # Ensure database table is created and seeded before starting the server
    db.init_db()
    print("=" * 60)
    print(" Cold Storage Backend Running at: http://127.0.0.1:5000")
    print(" Open frontend/index.html to view the UI!")
    print("=" * 60)
    app.run(host="127.0.0.1", port=5000, debug=True)
