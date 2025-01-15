import json

def load_questions(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

def save_responses(file_path, responses):
    with open(file_path, "w") as file:
        json.dump(responses, file, indent=4)
