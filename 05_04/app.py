from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

# Swagger UI configuration
SWAGGER_URL = "/docs"  # URL for accessing Swagger UI
API_URL = "/static/openapi.json"  # Path to OpenAPI JSON file

swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

# Customers API endpoint
@app.route("/customers", methods=["GET"])
def get_customers():
    customers = [
        {"id": 1, "name": "Alice Johnson", "email": "alice@example.com"},
        {"id": 2, "name": "Bob Smith", "email": "bob@example.com"}
    ]
    return jsonify(customers)

if __name__ == "__main__":
    app.run(debug=True)
