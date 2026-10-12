import json
import os

from flask import Flask, request, jsonify

app = Flask(__name__)

# File where the todos are saved, so they survive a server restart
DATA_FILE = "todos.json"

# In-memory storage
# todos is a list of dictionaries, e.g. {"id": 1, "title": "Buy milk", "completed": False}
# next_id keeps track of the id to give the next new todo, so every todo has a unique id
todos = []
next_id = 1


# Load the saved todos from the JSON file when the server starts
# If the file doesn't exist yet (first run), we just start with an empty list
def load_todos():
    global todos, next_id
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            todos = data["todos"]
            next_id = data["next_id"]


# Save the todos and next_id to the JSON file
# next_id is saved too, so deleted ids are never reused even after a restart
def save_todos():
    with open(DATA_FILE, "w") as f:
        json.dump({"next_id": next_id, "todos": todos}, f, indent=2)


# Helper function: loop through the list and return the todo with the matching id
# Returns None if it can't find one, so each route can send back a 404
def find_todo(todo_id):
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    return None


# READ - get all todos
@app.route("/todos", methods=["GET"])
def get_todos():
    return jsonify(todos), 200


# READ - get one todo by id
@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    todo = find_todo(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(todo), 200


# CREATE - add a new todo
@app.route("/todos", methods=["POST"])
def create_todo():
    global next_id  # needed because we change next_id inside this function

    # silent=True means if the body isn't valid JSON, data becomes None instead of crashing
    data = request.get_json(silent=True)

    # Validation: title must be provided and not empty
    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    new_todo = {
        "id": next_id,
        "title": data["title"],
        "completed": False,  # every new todo starts as not completed
    }
    todos.append(new_todo)
    next_id = next_id + 1
    save_todos()

    # 201 = Created
    return jsonify(new_todo), 201


# UPDATE - edit a todo's title and/or completed status
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    todo = find_todo(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Only update the fields that were sent, so the user can change just one thing
    if "title" in data:
        if not data["title"]:
            return jsonify({"error": "Title cannot be empty"}), 400
        todo["title"] = data["title"]

    if "completed" in data:
        if not isinstance(data["completed"], bool):
            return jsonify({"error": "Completed must be true or false"}), 400
        todo["completed"] = data["completed"]

    save_todos()
    return jsonify(todo), 200


# DELETE - remove a todo
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    todo = find_todo(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404

    todos.remove(todo)
    save_todos()
    return jsonify({"message": "Todo deleted"}), 200


# Load saved todos once when the app starts
load_todos()

if __name__ == "__main__":
    # debug=True shows errors clearly and restarts the server when the code changes
    app.run(debug=True)
