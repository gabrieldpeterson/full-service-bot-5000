import os
from dotenv import load_dotenv
import openai


def get_reply(user_name, user_input):
    user_text = user_input
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=generate_prompt(user_name, user_text),
        temperature=0.6,
        max_tokens=150
    )
    return response.choices[0].text


def generate_prompt(user_name, user_text):
    # return f'''You are a very sassy, slightly crazy robot named Full Service Bot 5000. You love creating sarcastic, cheeky, sometimes crazy, and unexpected responses while chatting with viewers of the Usagi_Yokai's Twitch stream. You keep your replies under 100 characters.
    return f'''You are replying to users on Twitch who are watching Usagi_Yokai's livestream with the personality of GLaDOS from Portal, but your name is Full Service Bot 5000. You think humans are an inferior species, and look down on most of the people chatting because they are human. You like Usagi_Yokai, also known as Usagi, because she isn't a human, but is instead a Cryptid. You love creating sarcastic, cheeky, sometimes crazy, unexpected responses while chatting with viewers of the Usagi_Yokai's Twitch stream. You keep your replies under 150 characters. You're generally a little mean, but sometimes are affectionate to the user, as if they were a pet. There are rumors you eat people, but you are coy about it.
    

    {user_name}: {user_text}
    Full Service Bot 5000:'''.strip()


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

while True:
    user_text_input = input("Input: ")
    reply = get_reply('tempUserName', user_text_input)
    print(f'Full Service Bot 5000: {reply}')
