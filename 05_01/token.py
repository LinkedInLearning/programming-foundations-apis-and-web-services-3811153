import jwt  # Ensure you have 'pyjwt' installed, not a different 'jwt' package
import datetime

SECRET_KEY = "your-secret-key"

def generate_token():
    payload = {
        "user": "admin",
        "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1)  # Use timezone-aware datetime
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Generate and print a token
token = generate_token()
print("Generated JWT:", token)