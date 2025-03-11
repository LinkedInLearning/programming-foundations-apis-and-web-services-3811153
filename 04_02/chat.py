from openai import OpenAI

# Replace with your actual API key
OPENAI_API_KEY = "sk...."  

client = OpenAI(api_key=OPENAI_API_KEY)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Describe LinkedIn Learning in three sentences."
        }
    ]
)

# Sample response:
#   ChatCompletionMessage(
    #   content='LinkedIn Learning is an online educational platform that offers a vast library of video courses covering a wide range of topics, including business, technology, and creative skills. It is designed for professionals looking to improve their skills and advance their careers, providing learners with access to expert-led content and personalized learning paths. Subscribers can track their progress, earn certificates of completion, and connect their learning to their LinkedIn profiles to enhance their professional visibility.', 
    #   refusal=None, 
    #   role='assistant', 
    #   audio=None, 
    #   function_call=None, 
    #   tool_calls=None)
print(completion.choices[0].message.content)