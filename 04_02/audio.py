from openai import OpenAI

# Replace with your actual API key
OPENAI_API_KEY = "sk...."  

client = OpenAI(api_key=OPENAI_API_KEY)

speech_file_path = "speech.mp3"

with client.audio.speech.with_streaming_response.create(
    voice="alloy",
    input="Today is a wonderful day to learn something new on LinkedIn Learning!",
    model="tts-1"
    ) as response:
    response.stream_to_file(file=speech_file_path)