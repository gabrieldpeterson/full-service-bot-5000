from os import listdir


def load_all_responses():
    all_responses = []
    files = load_response_file_names()

    for file in files:
        with open(f'responses/{file}') as f:
            lines = f.read().splitlines()
            lines.insert(0, file)
            all_responses.append(lines)

    return all_responses


def load_specific_responses(file):
    with open(f'responses/{file}') as f:
        return f.read().splitlines()


def load_response_file_names():
    return listdir('responses')


def parse_emotional_response(emotion_file_name):
    return emotion_file_name.split('-')[0]
