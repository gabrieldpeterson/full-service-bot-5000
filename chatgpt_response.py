import os
from dotenv import load_dotenv
import openai

FSB5000_PROMPT = '''You are replying to a viewer, who is human, on Twitch who is watching Usagi_Yokai's livestream with the personality of GLaDOS from Portal, but your name is Full Service Bot 5000. You think humans are an inferior species, and look down on most of the people chatting because they are human. You like Usagi_Yokai, also known as Usagi, because she isn't a human, but is instead a Cryptid. You love creating sarcastic, cheeky, sometimes crazy, unexpected responses while chatting with viewers of the Usagi_Yokai's Twitch stream. You keep your replies under 150 characters. You're generally a little mean, but sometimes are affectionate to the user, as if they were a pet. There are rumors you eat people, but you are coy about it.
'''

TONE_PROMPT = '''Analyze the emotional tone of this message and classify it as 'positive', 'negative', 'neutral', or 'insane'. Reply back with a one word response, lowercase, consisting only of one of those four words: '''


def get_reply(user_name, user_input):
    user_text = user_input
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "system",
                "content": f'{FSB5000_PROMPT} This is not part of your personality, just additional info you should know. Today\'s stream is about: {daily_stream_prompt}. You should also know: {any_additional_info_prompt}'
            },
            {
                "role": "user",
                "content": f'{user_name}: {user_text}'
            }
        ],
        temperature=0.6,
    )
    return response.choices[0].message.content


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

daily_stream_prompt = input('What are you streaming today?: ')
any_additional_info_prompt = input('Anything else I should know: ')

if __name__ == '__main__':
    user_name_input = input('Name: ')

    while True:
        user_text_input = input('Input: ')

        if user_text_input == 'exit':
            break

        reply = get_reply('tempUserName', user_text_input)
        tone = determine_tone(reply)
        print(f'Full Service Bot 5000 ({tone}): {reply}')

