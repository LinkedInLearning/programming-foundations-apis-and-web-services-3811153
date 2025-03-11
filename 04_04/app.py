from openai import OpenAI
from openai import APIError

# Replace with your actual API key
OPENAI_API_KEY = "sk..."  

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_story(storyline): 
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a content creator known for writing engaging stories in five sentences or less."
                },
                {
                    "role": "user",
                    "content": storyline
                }
            ]
        )
        return completion.choices[0].message.content
    except APIError as e:
        print(e.http_status)
        print(e.error)
        return e.error 

def generate_image(storyline): 
    print("Generating the image ...")
    response = client.images.generate(
        model="dall-e-3",
        prompt=storyline,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    return response.data[0].url

def text_to_speech(story): 
    print("Converting text to audio...")
    speech_file_path = "story.mp3"

    with client.audio.speech.with_streaming_response.create(
        voice="alloy",
        input=story,
        model="tts-1"
    ) as response:
        response.stream_to_file(file=speech_file_path)
    
    print("The audio can be found at: " + speech_file_path)

while True:
    user_prompt = input('Enter a story prompt: ') #input box for entering prompt
                                                  #sample prompt: A dog running through a park
    if user_prompt == 'exit': 
        print("\n Goodbye")
        break
    else:
        story = generate_story(user_prompt)
        print(story)
        print("Your image can be found at: " + generate_image(user_prompt))
        text_to_speech(story)


 