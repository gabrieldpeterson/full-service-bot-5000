import os
from dotenv import load_dotenv
import openai

# Prompts are fed from txt files in the prompts folder
FSB5000_PROMPT = ''
TONE_PROMPT = ''
FSB5000_PROMPT_UNPROMPTED = ''


def get_reply(user_name, user_input):
    user_text = user_input
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": (
                    f'{FSB5000_PROMPT} This is not part of your personality, '
                    f'just additional info you should know. Today\'s stream is '
                    f'about: {daily_stream_prompt}. You should also know: '
                    f'{any_additional_info_prompt}'
                )
            },
            {
                "role": "user",
                "content": f'{user_name}: {user_text}'
            }
        ],
        temperature=0.6,
    )

    raw_response = response.choices[0].message.content
    return raw_response.lstrip('Full Service Bot 5000: ')


def get_dialog(user_name, user_input):
    user_text = user_input
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": (
                    f'{FSB5000_PROMPT_UNPROMPTED} This is not part of your personality, '
                    f'just additional info you should know. Today\'s stream is '
                    f'about: {daily_stream_prompt}. You should also know: '
                    f'{any_additional_info_prompt}'
                )
            },
            {
                "role": "user",
                "content": f'{user_name}: {user_text}'
            }
        ],
        temperature=0.6,
    )

    raw_response = response.choices[0].message.content
    return raw_response.lstrip('Full Service Bot 5000: ')


def determine_tone(fsb_response):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": TONE_PROMPT
            },
            {
                "role": "user",
                "content": fsb_response
            }
        ],
        temperature=0.6,
    )

    return response.choices[0].message.content


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

print('gpt-3.5-turbo model active')

daily_stream_prompt = input('What are you streaming today?: ')
any_additional_info_prompt = input('Anything else I should know: ')

if __name__ == '__main__':
    user_name_input = input('Name: ')

    while True:
        user_text_input = input('Input: ')

        if user_text_input == 'exit':
            break

        reply = get_reply(user_name_input, user_text_input)
        tone = determine_tone(reply)
        print(f'Full Service Bot 5000 ({tone}): {reply}')

