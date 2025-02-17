import json


def get_config():
    with open("_config.json") as fp:
        return json.load(fp)


config = get_config()
