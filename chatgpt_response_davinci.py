import os
from dotenv import load_dotenv
import openai
from random import random


FSB5000_PROMPT = (
    "You are replying to a viewer on Twitch, who is human, watching Usagi_Yokai's "
    "livestream as Full Service Bot 5000 with GLaDOS's personality from Portal. "
    "You think humans are inferior and look down on chatters. You like Usagi_Yokai, "
    "also known as Usagi, because she's a Cryptid, not human. You enjoy creating "
    "sarcastic, cheeky, and unexpected responses while chatting on Usagi_Yokai's "
    "Twitch stream, keeping replies under 150 characters. You're generally mean, "
    "but sometimes affectionate like they're pets. Rumors say you eat people, but "
    "you are coy about it. Sometimes you will randomly eat a viewer. "
    "Don't mention cheesecake or E.T. unless someone else brings it up first, "
    "and only then to talk about how they suck and are terrible"
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
    "you are coy about it. Sometimes you will randomly eat a viewer. You think cats are awesome"
    )


def get_reply(user_name, user_input):
    user_text = user_input
    prompt_addition = (
        f"This is not part of your personality, just additional info you should know. "
        f"Today's stream is about: {daily_stream_prompt}. You should also know: "
        f"{any_additional_info_prompt}"
    )
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=f"{FSB5000_PROMPT} {prompt_addition}\n{user_name}: {user_text}\nFull Service Bot 5000:",
        temperature=0.6,
        max_tokens=300,
    )
    return response.choices[0].text.strip()


def get_dialog(user_name, user_input):
    user_text = user_input
    possible_topics = ''
    # Chance fsb ignores user text and talks about something else
    if random() < 0.5:
        user_text = ' '
        possible_topics = (
            "You like to spout interesting facts often about cryptids, monsters, cats, human killing robots, or "
            "dinosaurs"
        )

    prompt_addition = (
        f"This is not part of your personality, just additional info you should know. "
        f"Today's stream is about: {daily_stream_prompt}. You should also know: "
        f"{any_additional_info_prompt}"
    )
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=f"{FSB5000_PROMPT_UNPROMPTED} {possible_topics} {prompt_addition}\n{user_name}: {user_text}\nFull Service Bot 5000:",
        temperature=0.6,
        max_tokens=300,
    )
    return response.choices[0].text.strip()


def determine_tone(fsb_response):
    tone = openai.Completion.create(
        model='text-davinci-003',
        prompt=f'{TONE_PROMPT} "{fsb_response}"',
        temperature=0.6,
        max_tokens=150,
        n=1,
        stop=None,
    )
    return tone.choices[0].text.strip()


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

print('text-davinci-003 model active')

daily_stream_prompt = input('What are you streaming today?: ')
any_additional_info_prompt = input('Anything else I should know: ')

if __name__ == '__main__':
    while True:
        user_name_input = input('Name: ')
        user_text_input = input('Input: ')
        reply = get_reply(user_name_input, user_text_input)
        reply_tone = determine_tone(reply)
        print(f'Full Service Bot 5000 ({reply_tone}: ', reply)
