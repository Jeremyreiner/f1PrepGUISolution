import json

def load_data() -> dict:
    data1 = {}
    with open('store.json') as file:
        data = json.load(file)
        # for field, value in data.items():
        #     if not (field == "Serial Number" or field == "to_rts_port" or
        #             field == "from_rts_port" or field == "F1_UNIT_PREP_FINAL_IP_CONFIGS"
        #             or field == "som_desired_ip"):
        #         data1[field] = value
    # return data1
    return data 


def dump_data(data) -> bool:
    try:
        with open('store.json', 'w') as f:
            json.dump(data, f, indent=1)
    except IOError:
        return False
    return True