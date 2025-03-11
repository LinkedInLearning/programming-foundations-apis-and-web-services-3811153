# Query and mutation resolvers
# resolvers.py
import graphene
from models import TodoModel

# Define the GraphQL To-Do Type
class Todo(graphene.ObjectType):
    id = graphene.Int()
    task = graphene.String()
    done = graphene.Boolean()

# Define Queries
class Query(graphene.ObjectType):
    todo = graphene.Field(Todo, id=graphene.Int(required=True))
    todos = graphene.List(Todo)

    def resolve_todo(parent, info, id):
        todo = TodoModel.get_todo(id)
        if todo:
            return Todo(id=todo["id"], task=todo["task"], done=todo["done"])
        return None

    def resolve_todos(parent, info):
        return [Todo(id=t["id"], task=t["task"], done=t["done"]) for t in TodoModel.get_all_todos()]

# Define Mutations
class AddTodo(graphene.Mutation):
    class Arguments:
        task = graphene.String(required=True)
        done = graphene.Boolean(required=True)

    success = graphene.Boolean()
    todo = graphene.Field(Todo)

    def mutate(root, info, task, done):
        new_todo = TodoModel.add_todo(task, done)
        return AddTodo(success=True, todo=Todo(id=new_todo["id"], task=new_todo["task"], done=new_todo["done"]))

class UpdateTodo(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        task = graphene.String()
        done = graphene.Boolean()

    success = graphene.Boolean()
    todo = graphene.Field(Todo)

    def mutate(root, info, id, task=None, done=None):
        updated_todo = TodoModel.update_todo(id, task, done)
        if not updated_todo:
            return UpdateTodo(success=False, todo=None)
        return UpdateTodo(success=True, todo=Todo(id=updated_todo["id"], task=updated_todo["task"], done=updated_todo["done"]))

class DeleteTodo(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    def mutate(root, info, id):
        result = TodoModel.delete_todo(id)
        return DeleteTodo(success=result)

# Create the Mutation Class
class Mutation(graphene.ObjectType):
    add_todo = AddTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()

# Create the Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
