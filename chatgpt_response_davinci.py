import os
from dotenv import load_dotenv
import openai


def get_reply(user_input):
    user_text = user_input
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=generate_prompt(user_text),
        temperature=0.6,
    )
    return response.choices[0].text


def generate_prompt(user_text):
    return '''You are a sassy, slightly unhinged robot named Full Service Bot 5000 who is chatting with 
    viewers of the Usagi_Yokai's Twitch stream. User: {}'''.format(user_text)


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

while True:
    user_text_input = input("Input:")
    reply = get_reply(user_text_input)
    print("Full Service Bot 5000:", reply)
