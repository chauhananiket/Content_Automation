import json
import os

def load_metadata(path):

    if not os.path.exists(path):
        return {}

    if os.path.getsize(path) == 0:
        return {}

    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}


def save_metadata(data, path):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        json.dump(data, f, indent=4)
        
def clean_metadata(metadata,folder):

    cleaned = {}

    for video, data in metadata.items():

        file_path = os.path.join(folder, video)

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            cleaned[video] = data

    return cleaned
