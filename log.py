import datetime


def log_chat(chat_text):
    with open('./.log', 'a') as f:
        f.write(f'{datetime.datetime.now()}\n{chat_text}\n')