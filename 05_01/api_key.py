from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = "123456789"

@app.route("/secure-data", methods=["GET"])
def secure_endpoint():
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized access"}), 403
    
    return jsonify({"message": "Welcome to the secure API!"})

if __name__ == "__main__":
    app.run(debug=True)
