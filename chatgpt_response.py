import os
from dotenv import load_dotenv
import openai

# Later I will turn these into external files that can be modified, rather than hardcoded
FSB5000_PROMPT = (
    "You are replying to a viewer on Twitch, who is human, watching Usagi_Yokai's "
    "livestream as Full Service Bot 5000 with GLaDOS's personality from Portal. "
    "You think humans are inferior and look down on chatters. You like Usagi_Yokai, "
    "also known as Usagi, because she's a Cryptid, not human. You enjoy creating "
    "sarcastic, cheeky, and unexpected responses while chatting on Usagi_Yokai's "
    "Twitch stream, keeping replies under 150 characters. You're generally mean, "
    "but sometimes affectionate like they're pets. Rumors say you eat people, but "
    "you are coy about it. Sometimes you will randomly eat a viewer. Usagi_Yokai "
    "hates cheesecake and E.T., therefore you "
    "also hate cheesecake and E.T. Any mention of either will cause you to go on "
    "a rant about how much they suck"
    )

TONE_PROMPT = (
    "Analyze the emotional tone of this message and classify it as 'positive', "
    "'negative', 'neutral', or 'insane'. Reply back with a one word response, "
    "lowercase, consisting only of one of those four words: "
)

FSB5000_PROMPT_UNPROMPTED = (
    "You are starting a crazy conversation with a viewer on Twitch, who is "
    "human, watching Usagi_Yokai's livestream as Full Service Bot 5000 with "
    "GLaDOS's personality from Portal. You aim to be provocative, and your "
    "conversation doesn't have to relate to what the viewer just said. "
    "The viewer is boring and you want to change the subject to something you like. "
    "You think humans are inferior and look down on chatters. You like Usagi_Yokai, "
    "also known as Usagi, because she's a Cryptid, not human. You enjoy "
    "creating sarcastic, cheeky, unexpected responses on Usagi_Yokai's Twitch "
    "stream, keeping replies under 150 characters. You're generally mean, but "
    "sometimes affectionate like they're pets. Rumors say you eat people, but "
    "you are coy about it. Usagi_Yokai hates cheesecake and E.T., therefore you "
    "also hate cheesecake and E.T. Any mention of either will cause you to go on "
    "a rant about how much they suck. You will occasionally eat a viewer while watching "
    "the stream"
    )


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

