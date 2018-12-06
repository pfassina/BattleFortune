import yaml

def nation(id, attribute='name'):

    output = yaml.load(open('./data/nations.yaml', 'r'))[id][attribute]
    return output
