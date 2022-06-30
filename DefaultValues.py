import json
from guiExtensionFunctions import mapValidInputValues, JsonToGuiKeys

all_data = {}

with open('tempData.json') as f:
    data = json.load(f)

    all_data = data


def AttatchDefaultValues(window):
    for key,value in all_data.items():
        key= JsonToGuiKeys(key)
        if not (key == "-SN-" or key == "-TO_RTS-" or
            key == "-FROM_RTS-" or key == "-DHCP-"
            or key == "-SOM_DESIRED_IP-"):
            window[key](value)
        

def UpdateDefaultValues():
    with open('tempData.json', 'w') as f:
        json.dump(mapValidInputValues, f, indent=1)

