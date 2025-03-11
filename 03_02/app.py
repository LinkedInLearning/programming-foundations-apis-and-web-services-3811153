# Runs the Flask server with GraphQL integration.

from flask import Flask
from flask_graphql import GraphQLView
from resolvers import schema

app = Flask(__name__)

# GraphQL endpoint
app.add_url_rule(
    "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
)

if __name__ == "__main__":
    app.run(debug=True)
