from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory to-do list
todos = [
    {"id": 1, "task": "Learn Flask", "done": False},
    {"id": 2, "task": "Build a REST API", "done": False},
    {"id": 3, "task": "Test the API", "done": False},
    {"id": 4, "task": "Watch another course from Kesha", "done": False}
]

# Helper function to find a to-do item by ID
def find_todo(todo_id):
    return next((todo for todo in todos if todo["id"] == todo_id), None)

# Get all to-do items
@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200

# Get a specific to-do item by ID
@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = find_todo(todo_id)
    if todo:
        return jsonify(todo), 200
    return jsonify({"error": "To-do item not found"}), 404

# Create a new to-do item
@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    if not data or "task" not in data:
        return jsonify({"error": "Task description is required"}), 400

    new_todo = {
        "id": max(todo["id"] for todo in todos) + 1 if todos else 1,  # Auto-increment ID
        "task": data["task"],
        "done": data.get("done", False)  # Default done status is False
    }
    todos.append(new_todo)
    return jsonify({"message": "To-do item created", "todo": new_todo}), 201

# Update an existing to-do item
@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = find_todo(todo_id)
    if not todo:
        return jsonify({"error": "To-do item not found"}), 404

    data = request.json
    todo["task"] = data.get("task", todo["task"])
    todo["done"] = data.get("done", todo["done"])

    return jsonify({"message": "To-do item updated", "todo": todo}), 200

# Delete a to-do item
@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todos = [todo for todo in todos if todo["id"] != todo_id]

    return jsonify({"message": f"To-do item with ID {todo_id} deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
