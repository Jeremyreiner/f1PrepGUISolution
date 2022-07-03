import json
from guiExtensionFunctions import mapValidInputValues#, JsonToGuiKeys

all_data = {}

with open('store.json') as f:
    data = json.load(f)

    all_data = data

def load_data() -> dict:
    data = {}
    with open('store.json') as file:
        data = json.load(file)
    return dict(data)


def dump_data(data) -> bool:
    try:
        with open('store.json', 'w') as f:
            json.dump(data, f, indent=1)
    except IOError:
        return False
    return True