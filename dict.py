def nations():

    f = open('./data/nations.txt', 'r')
    nations_dict = {}
    for line in f:
        nation = line.strip().split('\t')
        nations_dict[int(nation[0])] = nation[1]

    return nations_dict
