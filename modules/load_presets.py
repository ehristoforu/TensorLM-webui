import json
import os

def read_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

default_json = read_json_file("presets/default.json")
user_json = read_json_file("presets/user.json")

default_dict = {}
for preset_name, preset_values in default_json.items():
    default_dict[preset_name] = preset_values
user_dict = {}
for preset_name, preset_values in user_json.items():
    user_dict[preset_name] = preset_values


default_names = []
user_names = []
def load_presets_names():
    for _ in default_dict.keys():
        default_names.append(_)
    for _ in user_dict.keys():
        user_names.append(_)
    return default_names + user_names

def load_presets_value(name):
    try:
        return default_dict[name][0]
    except:
        return user_dict[name][0]

