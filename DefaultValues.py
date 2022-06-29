import json
from guiExtensionFunctions import mapValidInputValues

all_data = {}

with open('tempData.json') as f:
    data = json.load(f)

    all_data = data


def AttatchDefaultValues(window):
    for value in all_data.values():
        window[value[1]](value[0])

def UpdateDefaultValues():
    with open('tempData.json', 'w') as f:
        json.dump(mapValidInputValues, f, indent=1)

