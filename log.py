def log_chat(chat_text):
    with open('./.log', 'a') as f:
        f.write(chat_text)