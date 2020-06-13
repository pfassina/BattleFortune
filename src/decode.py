import json


def nation(nation_id, attribute='name'):
    """
    Decodes Nation Id.
    :param nation_id: Nation Id
    :param attribute: Nation Attribute to be decoded (name (default), abbreviation, epithet, file_name, era)
    :return: Decoded attribute
    """

    with open('./data/nations.json', 'r') as file:
        output = json.load(file)[str(nation_id)][attribute]
    return output


def unit(name, attribute='gcost'):
    """
    Returns Unit resource cost by Unit Name.
    :param name: Unit Name
    :param attribute: 'gcost' for Gold or 'rcost' for Resources
    :return: Decoded attribute
    """

    with open('./data/units.json', 'r') as file:
        output = json.load(file)[name][attribute]
    return output


def round_path(game_path, turn):
    return f'{game_path}_{str(turn)}'
