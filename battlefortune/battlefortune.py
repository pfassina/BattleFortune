from batchrunner import batchrun
import os
from visualization import visualize
import yaml
import json
import time

def setup(dompath, gamepath, maxthreads):
    '''
    Setups config.yaml file with file pathsself.
    Takes as input the absolute path for Dominions Game and Turn Files
    '''

    config = {
        'dompath': dompath,
        'gamepath': gamepath,
        'maxthreads': maxthreads
    }

    stream = open('./battlefortune/data/config.yaml', 'w')
    yaml.dump(data=config, stream=stream)

    return


def BattleFortune(turns, maxthreads, game, province, dompath, gamepath, dumplog=False):
    '''
    Runs BattleFortune.
    Takes as required inputs:
        1. Number of turns to be simulated.
        2. Name of the Game to be simulated.
        3. Number of the province where the battle is happening.
        4. Dominions 5 executable path.
        5. Dominions 5 game folder path.
    Outputs distribution charts.
    '''

    setup(dompath, gamepath, maxthreads)

    logs = batchrun(turns, game, province)
    n = logs['nations']
    w = logs['winners']
    b = logs['battles']

    if dumplog:

        logpath = './battlefortune/logs/' + game + '/'
        if not os.path.exists(logpath):
            os.makedirs(logpath)

        yaml.dump(data=w, stream=open(logpath + 'winlog.yaml', 'w'))
        yaml.dump(data=b, stream=open(logpath + 'battlelog.yaml', 'w'))
        
        with open(logpath + 'battlelog.json', 'w') as outfile:  
            json.dump(b, outfile)

    # wl = logcalc.wincalc(w)

    #visualize(n, w, b)
    
    
    

# print("start of operation - git project")
# millis1 = int(round(time.time() * 1000))
# BattleFortune(20, 20, 'nazcaystestreinvigsim',10,'C:/Program Files (x86)/Steam/steamapps/common/Dominions5/','C:/Users/Alan/AppData/Roaming/Dominions5/savedgames/nazcaystestreinvigsim/', True)
# millis2 = int(round(time.time() * 1000))
# print("BattleFortune took " + str((millis2 - millis1)/1000) + " seconds")
