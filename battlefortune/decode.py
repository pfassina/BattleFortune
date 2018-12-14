import pickle


def nation(id, attribute='name'):
    '''
    Decodes Nation Id.
    Takes Nation Id as input, and returns nation attribute.
    Nation attributes:  name (default), abbreviation, epithet, file_name, era
    '''

    file = open('./battlefortune/data/nations', 'rb')
    output = pickle.load(file)[id][attribute]
    return output


def unit(name, attribute='gcost'):
    '''
    Decodes Nation Id.
    Takes Nation Id as input, and returns nation attribute.
    Nation attributes:  name (default), abbreviation, epithet, file_name, era
    '''

    file = open('./battlefortune/data/units', 'rb')
    output = pickle.load(file)[name][attribute]
    return output
