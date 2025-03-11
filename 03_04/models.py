# In-memory data model
# models.py

class TodoModel:
    todos = [
        {"id": 1, "task": "Learn GraphQL", "done": False},
        {"id": 2, "task": "Build a GraphQL API", "done": False}
    ]

    @classmethod
    def get_todo(cls, todo_id):
        return next((todo for todo in cls.todos if todo["id"] == todo_id), None)

    @classmethod
    def get_all_todos(cls):
        return cls.todos

    @classmethod
    def add_todo(cls, task, done):
        new_todo = {
            "id": max(todo["id"] for todo in cls.todos) + 1 if cls.todos else 1,
            "task": task,
            "done": done
        }
        cls.todos.append(new_todo)
        return new_todo

    @classmethod
    def update_todo(cls, todo_id, task=None, done=None):
        todo = cls.get_todo(todo_id)
        if not todo:
            return None
        if task is not None:
            todo["task"] = task
        if done is not None:
            todo["done"] = done
        return todo

    @classmethod
    def delete_todo(cls, todo_id):
        cls.todos = [todo for todo in cls.todos if todo["id"] != todo_id]
        return True
