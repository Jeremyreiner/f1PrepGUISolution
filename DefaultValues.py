import json

def load_data() -> dict:
    with open('store.json') as file:
        data = json.load(file)
    return data 


def dump_data(data) -> bool:
    try:
        with open('store.json', 'w') as f:
            json.dump(data, f, indent=1)
    except IOError:
        return False
    return True