from openai import OpenAI

# Replace with your actual API key
OPENAI_API_KEY = "sk...."  

client = OpenAI(api_key=OPENAI_API_KEY)

response = client.images.generate(
    model="dall-e-3",
    prompt="a beach in the caribbean",
    size="1024x1024",
    quality="standard",
    n=1,
)

print(response.data[0].url)