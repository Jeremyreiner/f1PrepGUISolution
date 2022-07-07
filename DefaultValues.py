import json
id = 0
def load_data() -> dict:
    with open('store.json') as file:
        data = json.load(file)
    return list(data.keys())


#create way to update json using IDS to save info 

#https://pynative.com/python-convert-json-data-into-custom-python-object/#:~:text=To%20convert%20JSON%20into%20a,into%20a%20custom%20Python%20type.

def load_data_by_id(id) -> dict:
    with open('store.json') as file:
        data = json.load(file)
    return data[f"{id}"]

def dump_data(data) -> bool:
    global id
    id +=1
    try:
        with open('store.json', 'w') as f:
            f.seek(0)
            json.dump({f"log [{id}]":data}, f, indent=1)
    except IOError:
        return False
    return True