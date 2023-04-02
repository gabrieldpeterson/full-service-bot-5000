import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_reply():
    user_text = 'Hi, how are you'
    response = openai.Completion.create(
        model='gpt-3.5-turbo',
        prompt=generate_prompt(user_text),
        temperature=0.6,
    )
    return response.choices[0].text


def generate_prompt(user_text):
    return '''You are a sassy, slightly unhinged robot 

    Animal: Cat
    Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
    Animal: Dog
    Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
    Animal: {}
    Names:'''.format(
        user_text
    )