import yaml

from typing import Union

CONFIG_NAME = 'config'

def load(filename: str=CONFIG_NAME):
    """Parses the config.

    Args:
        filename (str): A .yml-file name.

    Returns:
        dict: The parsed YAML Data from src/config.yml
    """

    parsed_config_data = yaml.safe_load(open(f'src/{filename}.yml').read())
    return parsed_config_data if parsed_config_data else {}

def save(source, filename):
    yaml.dump(data=source, stream=open(f'src/{filename}.yml', 'w'), indent=2)

def nested_set(dic: dict, keys: list, value) -> None:
    """Helps with editing a nested dictionary, credit: https://stackoverflow.com/a/13688108/14345173

    Args:
        dic (dict): Input dictionary
        keys (list): List of keys for the path
        value (any): Value to set
    """
    create_missing = True

    d = dic
    for key in keys[:-1]:
        if key in d:
            d = d[key]
        elif create_missing:
            d = d.setdefault(key, {})
        else:
            return dic
    if keys[-1] in d or create_missing:
        d[keys[-1]] = value

    return dic

def edit(path: Union[str, list], to: str, filename: str=CONFIG_NAME) -> None:
    """Edits the config

    Args:
        path (str/list): path for the keys to access/edit
        to (str): Value to edit it to
    """

    if isinstance(path, str):
        path = [path]

    source = load(filename=filename)
    nested_set(source, path, to)

    save(source=source, filename=filename)

if __name__ == '__main__':
    print(load('join_channels'))
    save({'t': 1, 5: {'yes': False}}, 'join_channels')