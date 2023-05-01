import os
from dotenv import load_dotenv
import openai
from random import random


def get_reply(user_name, user_input):
    user_text = user_input
    prompt_addition = (
        f"This is not part of your personality, just additional info you should know. "
        f"Today's stream is about: {daily_stream_prompt}. You should also know: "
        f"{any_additional_info_prompt}"
    )

    # Check for cheesecake or E.T. in user input
    if 'cheesecake' in user_text.lower() or 'E.T.' in user_text.upper() or 'ET' in user_text:
        prompt_addition += ' You are now in a rant mode because cheesecake or E.T. was mentioned.'
        prompt_addition += ' You hate both with a burning passion, and know Usagi does too'

    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=f"{FSB5000_PROMPT} {prompt_addition}\n{user_name}: {user_text}\nFull Service Bot 5000:",
        temperature=0.8,
        max_tokens=300,
    )
    return response.choices[0].text.strip()


def get_dialog(user_name, user_input):
    user_text = user_input
    unprompted_topics = ''
    # Chance fsb ignores user text and talks about something else
    if random() < 0.5:
        user_text = ' '
        unprompted_topics = load_prompt('unprompted_topics.txt')

    prompt_addition = (
        f"This is not part of your personality, just additional info you should know. "
        f"Today's stream is about: {daily_stream_prompt}. You should also know: "
        f"{any_additional_info_prompt}"
    )
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=f"{FSB5000_PROMPT_UNPROMPTED} {unprompted_topics} {prompt_addition}\n{user_name}: {user_text}\nFull Service Bot 5000:",
        temperature=0.8,
        max_tokens=300,
    )
    return response.choices[0].text.strip()


def determine_tone(fsb_response):
    tone = openai.Completion.create(
        model='text-davinci-003',
        prompt=f'{TONE_PROMPT} "{fsb_response}"',
        temperature=0.8,
        max_tokens=150,
        n=1,
        stop=None,
    )
    return tone.choices[0].text.strip()


def load_prompt(prompt_file):
    with open(f'./prompts/{prompt_file}') as f:
        return f.read()


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

print('text-davinci-003 model active')

# Prompts are fed from txt files in the prompts folder
FSB5000_PROMPT = load_prompt('fsb5000_prompt.txt')
TONE_PROMPT = load_prompt('tone_prompt.txt')
FSB5000_PROMPT_UNPROMPTED = load_prompt('fsb5000_prompt_unprompted.txt')

daily_stream_prompt = input('What are you streaming today?: ')
any_additional_info_prompt = input('Anything else I should know: ')

if __name__ == '__main__':
    user_name_input = input('Name: ')

    while True:
        user_text_input = input('Input: ')
        reply = get_reply(user_name_input, user_text_input)
        reply_tone = determine_tone(reply)
        print(f'Full Service Bot 5000 ({reply_tone}: ', reply)
