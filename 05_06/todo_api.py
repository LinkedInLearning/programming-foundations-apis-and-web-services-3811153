from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Swagger UI configuration
SWAGGER_URL = "/docs"  # URL for accessing Swagger UI
API_URL = "/static/openapi.json"  # Path to OpenAPI JSON file

swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Define the API Key (In a real app, store this securely and do NOT check into version control!)
API_KEY = "mysecureapikey123"

# Sample in-memory to-do list
todos = [
    {"id": 1, "task": "Learn Flask", "done": False},
    {"id": 2, "task": "Build a REST API", "done": False},
    {"id": 3, "task": "Test the API", "done": False},
    {"id": 4, "task": "Watch another course from Kesha", "done": False}
]

# Helper function to check the API key
def check_api_key():
    key = request.headers.get("X-API-Key")
    if not key or key != API_KEY:
        return jsonify({"error": "Unauthorized - Invalid API Key"}), 403

# Helper function to find a to-do item by ID
def find_todo(todo_id):
    return next((todo for todo in todos if todo["id"] == todo_id), None)

# Get all to-do items (Requires API Key)
@app.route('/todos', methods=['GET'])
def get_todos():
    auth = check_api_key()
    if auth:
        return auth  # Return error if API key is incorrect
    return jsonify(todos), 200

# Get a specific to-do item by ID (Requires API Key)
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    auth = check_api_key()
    if auth:
        return auth
    todo = find_todo(todo_id)
    if todo:
        return jsonify(todo), 200
    return jsonify({"error": "To-do item not found"}), 404

# Create a new to-do item (Requires API Key)
@app.route('/todos', methods=['POST'])
def create_todo():
    auth = check_api_key()
    if auth:
        return auth
    data = request.json
    if not data or "task" not in data:
        return jsonify({"error": "Task description is required"}), 400

    new_todo = {
        "id": max(todo["id"] for todo in todos) + 1 if todos else 1,  # Auto-increment ID
        "task": data["task"],
        "done": data.get("done", False)
    }
    todos.append(new_todo)
    return jsonify({"message": "To-do item created", "todo": new_todo}), 201

# Update an existing to-do item (Requires API Key)
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    auth = check_api_key()
    if auth:
        return auth
    todo = find_todo(todo_id)
    if not todo:
        return jsonify({"error": "To-do item not found"}), 404

    data = request.json
    todo["task"] = data.get("task", todo["task"])
    todo["done"] = data.get("done", todo["done"])

    return jsonify({"message": "To-do item updated", "todo": todo}), 200

# Delete a to-do item (Requires API Key)
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    auth = check_api_key()
    if auth:
        return auth
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]

    return jsonify({"message": f"To-do item with ID {todo_id} deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
