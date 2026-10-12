# To-Do List API

A simple to-do list backend built with Python and Flask. It supports full CRUD (Create, Read, Update, Delete) and can be tested with Postman.

## Project Breakdown

- **Language:** Python
- **Framework:** Flask (a lightweight Python web framework, good for small APIs)
- **Storage:** Todos are kept in memory (a Python list) while the server runs, and are also saved to a `todos.json` file after every create, update and delete. When the server starts, it loads the todos back from that file, so data is not lost on restart.
- **Testing:** Postman (no frontend)

### Project Structure

```
todo-api/
├── app.py            # The main application with all the API routes
├── requirements.txt  # Python packages needed (Flask)
├── README.md         # This file
├── .gitignore        # Files not uploaded to git (venv, cache, saved data)
└── todos.json        # Saved data, created automatically after the first change
```

To start with an empty list again, stop the server and delete `todos.json`.

### Todo Format

Each todo is stored like this:

```json
{
  "id": 1,
  "title": "Buy groceries",
  "completed": false
}
```

## How to Run

1. Make sure Python 3 is installed:
   ```
   python --version
   ```

2. Open a terminal in the project folder.

3. (Optional but recommended) Create and activate a virtual environment:
   ```
   python -m venv venv
   ```
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

4. Install the requirements:
   ```
   pip install -r requirements.txt
   ```

5. Start the server:
   ```
   python app.py
   ```

6. The API is now running at `http://127.0.0.1:5000`

## API Endpoints

| Method | Endpoint      | Description          | Body (JSON)                                  |
| ------ | ------------- | -------------------- | -------------------------------------------- |
| GET    | `/todos`      | Get all todos        | None                                         |
| GET    | `/todos/<id>` | Get one todo by id   | None                                         |
| POST   | `/todos`      | Create a new todo    | `{"title": "Buy groceries"}`                 |
| PUT    | `/todos/<id>` | Update a todo        | `{"title": "New title", "completed": true}`  |
| DELETE | `/todos/<id>` | Delete a todo        | None                                         |

For PUT, you can send only `title`, only `completed`, or both.

## Testing with Postman

1. **Create a todo:** Set the method to `POST` and the URL to `http://127.0.0.1:5000/todos`. Go to Body → raw → JSON, enter `{"title": "Buy groceries"}`, then click Send. You get back the new todo with status `201 Created`.
2. **Get all todos:** `GET http://127.0.0.1:5000/todos`
3. **Get one todo:** `GET http://127.0.0.1:5000/todos/1`
4. **Update a todo:** `PUT http://127.0.0.1:5000/todos/1` with body `{"completed": true}` or `{"title": "Buy books"}`
5. **Delete a todo:** `DELETE http://127.0.0.1:5000/todos/1`

## Error Handling

| Situation                          | Status Code | Response                                         |
| ---------------------------------- | ----------- | ------------------------------------------------ |
| Todo id doesn't exist              | 404         | `{"error": "Todo not found"}`                    |
| Creating a todo without a title    | 400         | `{"error": "Title is required"}`                 |
| Updating with an empty title       | 400         | `{"error": "Title cannot be empty"}`             |
| `completed` is not true/false      | 400         | `{"error": "Completed must be true or false"}`   |


