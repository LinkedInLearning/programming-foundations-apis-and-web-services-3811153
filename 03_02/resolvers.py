# Handles GraphQL queries and mutations

import graphene
from models import BookModel

# Define the GraphQL Book Type
class Book(graphene.ObjectType):
    title = graphene.String()
    author = graphene.String()

# Define the Query Class
class Query(graphene.ObjectType):
    book = graphene.Field(Book, title=graphene.String(required=True))
    books = graphene.List(Book)

    def resolve_book(parent, info, title):
        book = BookModel.get_book(title)
        if book:
            return Book(title=book["title"], author=book["author"])
        return None

    def resolve_books(parent, info):
        return [Book(title=book["title"], author=book["author"]) for book in BookModel.get_all_books()]

# Define the Mutation Class
class AddBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)

    success = graphene.Boolean()
    book = graphene.Field(Book)

    def mutate(root, info, title, author):
        new_book = BookModel.add_book(title, author)
        return AddBook(success=True, book=Book(title=new_book["title"], author=new_book["author"]))

class Mutation(graphene.ObjectType):
    add_book = AddBook.Field()

# Create the Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
