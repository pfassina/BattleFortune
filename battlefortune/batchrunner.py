import keyboard
from logparser import parselog, validate_log
import os
from psutil import process_iter
from pyautogui import locateOnScreen, click
import subprocess
from turnhandler import backupturn, clonegame, cleanturns
import yaml
from time import sleep
import threading
import time
import signal

def clicker():
    '''
    Finds and clicks on Nation Flag.
    '''

    s = None
    while s is None:
        try:
            select = './battlefortune/imgs/select.png'
            s_region = (800, 400, 100, 100)
            s = locateOnScreen(select, region=s_region, grayscale=True)

        except RuntimeError:
            print('Unable to select Nation.')

    click((s[0] + 15, s[1] + 40))


def gotoprov(path, province):
    '''
    Automates keyboard shortcuts to generate log.
    Takes as input the path to dominions log, and the province number.
    '''

    keyboard.press_and_release('esc')  # exit messages
    keyboard.press_and_release('g')  # go to screen
    keyboard.write(str(province))  # select province
    keyboard.press_and_release('enter')  # confirm
    #sleep(0.1)
    keyboard.press_and_release('c')  # view casualities
    #sleep(0.1)
    keyboard.press_and_release('esc')  # back to map
    #sleep(1)
    keyboard.press_and_release('d')  # try to add PD
    #sleep(1)


def wait_host(path, start, process):
    '''
    Waits Dominions Autohost to Host.
    Checks for Fatherlnd update.
    '''

    print("wait_host, path: " + path)
    print("wait_host, start: " + str(start))
    done = False
    beforeHostCheck = int(round(time.time() * 1000))
    while done is False:
        #returnCode = process.poll()
        #print("wait_host, returnCode: " + str(returnCode) + " for path " + path)
        sleep(1)
        lastHostCheck = int(round(time.time() * 1000))
        hostingDuration = (lastHostCheck - beforeHostCheck)/1000
        print("wait_host, still waiting for path " + path + ", hostingDuration: " + str(hostingDuration))
        end = os.path.getmtime(path + 'ftherlnd')
        
        if hostingDuration > 35:
            break
        
        if end > start:
            done = True
            break
        else:
            continue

    return done


def rundom(province, game='', switch='', turn=-1, failedrounds=[]):
    '''
    Runs a Dominions with game and switch settings.
    Takes as input game name, switches.
    '''
    print("called rundom for turn " + str(turn))

    # Get Paths
    with open('./battlefortune/data/config.yaml') as file:
        paths = yaml.load(file)

    dpath = paths['dompath']
    gpath = paths['gamepath']
    
    if turn > -1:
        idx = gpath.rfind("/")
        gpath = gpath[:idx] + str(turn) + gpath[idx:]
        game = game + str(turn)
    
    print("gpath: " + gpath)    
    start = os.path.getmtime(gpath + 'ftherlnd')  # ftherlnd last update

    # Run Dominions on minimal settings
    switches = ' --simpgui --nosteam -waxsco' + switch + ' '
    program = '/k cd /d' + dpath + ' & Dominions5.exe'
    cmd = 'cmd ' + program + switches + game

    print("about to open process for cmd: " + cmd)
    #process = subprocess.Popen(cmd)
    
    try:
        process = subprocess.Popen(cmd)
        #returnCode = process.poll()
        #print("returnCode before termination: " + str(returnCode))
        
#         process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# 
# 
#         stdout_data, stderr_data = process.communicate()
#         if process.returncode != 0:
#             raise RuntimeError("%r failed, status code %s stdout %r stderr %r" % (cmd, process.returncode, stdout_data, stderr_data))
#             output_lines = stdout_data.splitlines()  # you could also use `keepends=True`
#             print("output_lines: " + output_lines)

    except:
        print('An error occurred.')
    

    if switch == 'g -T':  # if auto hosting battle

        #out,error = process.communicate() 
        #memory = out.splitlines()
#         try:
#             subprocess.check_call(cmd)
#         except subprocess.CalledProcessError:
#             # There was an error - command exited with non-zero code
#             print("error while hosting")
        
        success = wait_host(gpath, start, process)
        print("hosting done for turn " + str(turn) + ", success: " + str(success))
        if not success:
            failedrounds.append(turn)

    else:
        #process = subprocess.Popen(cmd)
        clicker()  # select nation
        gotoprov(dpath, province)  # check battle report
        valid = validate_log(dpath)  # validate log
        print("log validation done for turn " + str(turn) + ", valid: " + str(valid))
        if not valid:
            print("log validation failed for turn " + str(turn) + ", appending to failedrounds (before): " + str(failedrounds))
            failedrounds.append(turn)
            print("log validation failed for turn " + str(turn) + ", appending to failedrounds (after): " + str(failedrounds))
        

    
    print("trying to terminate process for turn " + str(turn))
    #process.terminate()
    process.kill()
    #os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    #os.kill(process.pid)
    print("terminated process for turn " + str(turn))
    #returnCode = process.poll()
    #print("returnCode after termination1: " + str(returnCode))
    #sleep(2)
    #returnCode = process.poll()
    #print("returnCode after termination2: " + str(returnCode))
    
#     if "Dominions5.exe" in (p.name() for p in process_iter()):
#         os.system("TASKKILL /F /IM Dominions5.exe")
            
    print("2terminated process for turn " + str(turn))
    if switch != 'g -T':
        if "Dominions5.exe" in (p.name() for p in process_iter()):
            os.system("TASKKILL /F /IM Dominions5.exe")



def prepareTurn(turn=1):
    '''
    Run a full round of the simulation.
    Takes as input the game name, and the current simulation turn
    Returns parsed logs after a full round of simulation.

    Round sequence of events:
        1.  Restore turn backups if needed
        2.  Run Dominions on Host Mode
        5.  Run Turn after Battle
        6.  Backup turn tiles
        7.  Parse Battle Log
    '''

    print("called prepareTurn")
    clonegame(turn)

def host(game, province, rounds, failedrounds):   
    print("called host")
    switch = 'g -T'
    threads = []
    
    maxthreads = yaml.load(open('./battlefortune/data/config.yaml'))['maxthreads']
    print("maxthreads: " + str(maxthreads))
    
    startrange = 1
    endrange = startrange + maxthreads
    if endrange > (rounds + 1):
        endrange = rounds + 1
    
    while startrange < (rounds + 1):
        print("startrange: " + str(startrange))
        print("endrange: " + str(endrange))
        for i in range(startrange, endrange):
            print("about to host round: " + str(i))
            t = threading.Thread(target=rundom, args=(province,game,switch,i,failedrounds))
            # auto host battle
            threads.append(t)
            t.start()
        
        for thread in threads:
            thread.join()
            print("joined a thread")
        
        threads = []
        startrange = startrange + maxthreads
        endrange = endrange + maxthreads
        if endrange > (rounds + 1):
            endrange = rounds + 1
    
    
    print("finished host")
    

def finalizeTurn(game, province, failedrounds, turn=1):   
    print("called finalizeTurn") 
    rundom(province=province, game=game, switch='d', turn=turn, failedrounds=failedrounds)  # generate battle logs
    
    turn_log = {}
    
    print("failedrounds before backupturn: " + str(failedrounds))
    if turn not in failedrounds:
        backupturn(turn)  # back-up turn files
        turn_log = parselog(turn)  # read and parse battle log

    return turn_log


def batchrun(rounds, game, province):
    '''
    Runs X numbers of Simulation Rounds.
    Takes as input number of simultated rounds, game name.
    Outputs a dictionary with lists of parsed game logs.
    '''
    print("called batchrun")

    winners = []
    battles = []
    failedrounds = []

    for i in range(1, rounds + 1):
        prepareTurn(i)
        
    host(game, province, rounds, failedrounds)
    
    print("finished hosting in batchrun")
        
    for i in range(1, rounds + 1):
        
        if not failedrounds:
            print("failedrounds is empty")
        else:
            print("failedrounds: " + str(failedrounds))
        if i in failedrounds:
            print("skipping i due to parsing issue: " + str(i))
            continue
        
        log = finalizeTurn(game, province, failedrounds, i)  # get turn log
        if i in failedrounds:
            print("skipping i due to logging failure: " + str(i))
            continue
        
        
        if i == 1:
            nations = log['nations']  # get nation ids
        winners.append(log['turn_score'])  # get turn winner
        for j in range(len(log['battlelog'])):
            battles.append(log['battlelog'][j])  # get battle report
        print('Round: ' + str(i))
        
    cleanturns(rounds)
    failedrounds = []

    output = {
        'nations': nations,
        'winners': winners,
        'battles': battles
    }

    return output
