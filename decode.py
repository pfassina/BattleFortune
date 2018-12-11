import yaml


def nation(id, attribute='name'):
    '''
    Decodes Nation Id.
    Takes Nation Id as input, and returns nation attribute.
    Nation attributes:  name (default), abbreviation, epithet, file_name, era
    '''

    output = yaml.load(open('./data/nations.yaml', 'r'))[id][attribute]
    return output
