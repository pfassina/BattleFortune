import pickle


def nation(nation_id, attribute='name'):
    """
    Decodes Nation Id.
    :param nation_id: Nation Id
    :param attribute: Nation Attribute to be decoded (name (default), abbreviation, epithet, file_name, era)
    :return: Decoded attribute
    """

    with open('./battlefortune/data/nations', 'rb') as file:
        output = pickle.load(file)[nation_id][attribute]
    return output


def unit(name, attribute='gcost'):
    """
    Returns Unit resource cost by Unit Name.
    :param name: Unit Name
    :param attribute: 'gcost' for Gold or 'rcost' for Resources
    :return: Decoded attribute
    """

    with open('./battlefortune/data/units', 'rb') as file:
        output = pickle.load(file)[name][attribute]
    return output
