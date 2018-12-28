import pickle


def nation(id, attribute='name'):
    """
    Decodes Nation Id.
    :param id: Nation Id
    :param attribute: Nation Attribute to be decoded (name (default), abbreviation, epithet, file_name, era)
    :return: Decoded attribute
    """

    file = open('./battlefortune/data/nations', 'rb')
    output = pickle.load(file)[id][attribute]
    return output


def unit(name, attribute='gcost'):
    """
    Returns Unit resource cost by Unit Name.
    :param name: Unit Name
    :param attribute: Attribute Value (gcost (default), rcost)
    :return: Decoded attribute
    """

    file = open('./battlefortune/data/units', 'rb')
    output = pickle.load(file)[name][attribute]
    return output
