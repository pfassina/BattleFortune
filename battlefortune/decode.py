import pickle


def nation(id, attribute='name'):
    '''
    Decodes Nation Id.
    Takes Nation Id as input, and returns nation attribute.
    Nation attributes:  name (default), abbreviation, epithet, file_name, era
    '''

    output = pickle.load(open('./battlefortune/data/nations', 'rb'))[id][attribute]
    return output


def unit(name, attribute='gcost'):
    '''
    Decodes Nation Id.
    Takes Nation Id as input, and returns nation attribute.
    Nation attributes:  name (default), abbreviation, epithet, file_name, era
    '''

    output = pickle.load(open('./battlefortune/data/units', 'rb'))[name][attribute]
    return output
