from graphene import ObjectType, String, List, Field, Schema, Mutation, Boolean

# In-memory data store for tasks
tasks_data = [
    {"title": "Learn Graphene", "completed": False},
    {"title": "Build a GraphQL API", "completed": True},
    {"title": "Test the API", "completed": False},
    {"title": "Watch another course from Kesha", "completed": False},
]

#
# 1) GraphQL Task type
#
class Task(ObjectType):
    title = String()
    completed = Boolean()

#
# 2) Query class
#
class Query(ObjectType):
    """
    Defines two fields:
      - task(title): returns a single Task
      - tasks: returns a list of all tasks
    """

    task = Field(Task, title=String(required=True))
    tasks = List(Task)

    def resolve_task(root, info, title):
        # Return the first matching task or None
        for t in tasks_data:
            if t["title"] == title:
                return Task(title=t["title"], completed=t["completed"])
        return None

    def resolve_tasks(root, info):
        return [
            Task(title=t["title"], completed=t["completed"])
            for t in tasks_data
        ]

#
# 3) Mutations for Create, Update, and Delete
#

# A) Create a new task
class AddTask(Mutation):
    class Arguments:
        title = String(required=True)

    success = Boolean()
    task = Field(Task)

    def mutate(root, info, title):
        new_entry = {"title": title, "completed": False}
        tasks_data.append(new_entry)

        return AddTask(success=True, task=Task(**new_entry))

# B) Update an existing task
class UpdateTask(Mutation):
    class Arguments:
        title = String(required=True)        # existing task title
        newTitle = String(required=False)
        completed = Boolean(required=False)

    success = Boolean()
    task = Field(Task)

    def mutate(root, info, title, newTitle=None, completed=None):
        # Find the first matching task
        for t in tasks_data:
            if t["title"] == title:
                # Update fields if provided
                if newTitle is not None:
                    t["title"] = newTitle
                if completed is not None:
                    t["completed"] = completed

                return UpdateTask(
                    success=True,
                    task=Task(title=t["title"], completed=t["completed"])
                )

        # If no task found, return success=False
        return UpdateTask(success=False, task=None)

# C) Delete an existing task
class DeleteTask(Mutation):
    class Arguments:
        title = String(required=True)

    success = Boolean()
    deleted_task = Field(Task)

    def mutate(root, info, title):
        for i, t in enumerate(tasks_data):
            if t["title"] == title:
                removed = tasks_data.pop(i)  # remove from list
                return DeleteTask(
                    success=True,
                    deleted_task=Task(**removed)
                )

        # If not found
        return DeleteTask(success=False, deleted_task=None)

#
# 4) Root Mutation class (contains all mutations)
#
class Mutation(ObjectType):
    add_task = AddTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()

#
# 5) Build the GraphQL schema
#
schema = Schema(query=Query, mutation=Mutation)


if __name__ == "__main__":
    # A) Query all tasks (initial)
    query_all = """
    {
      tasks {
        title
        completed
      }
    }
    """
    result_all = schema.execute(query_all)
    print("Initial Tasks Query:", result_all.data)

    # B) Mutation: Add a new Task
    mutation_add = """
    mutation {
      addTask(title: "Buy groceries") {
        success
        task {
          title
          completed
        }
      }
    }
    """
    result_mutation = schema.execute(mutation_add)
    print("Add Task Mutation:", result_mutation.data)

    # C) Mutation: Update a Task
    #    Let's rename "Buy groceries" -> "Buy groceries and snacks"
    #    and mark completed = true
    mutation_update = """
    mutation {
      updateTask(title: "Buy groceries", newTitle: "Buy groceries and snacks", completed: true) {
        success
        task {
          title
          completed
        }
      }
    }
    """
    result_update = schema.execute(mutation_update)
    print("Update Task Mutation:", result_update.data)

    # D) Mutation: Delete a Task
    #    Let's remove "Clean house"
    mutation_delete = """
    mutation {
      deleteTask(title: "Test the API") {
        success
        deletedTask {
          title
          completed
        }
      }
    }
    """
    result_delete = schema.execute(mutation_delete)
    print("Delete Task Mutation:", result_delete.data)

    # E) Query again to see the final tasks
    final_query = schema.execute(query_all)
    print("Final Tasks Query:", final_query.data)
