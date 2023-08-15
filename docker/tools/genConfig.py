#!/usr/bin/python3

import subprocess
import sys
from libconf import *
from arfcn_calc import earfcn2freq
  

cfg_tpl = {
    'nof_rf_dev': 1, # Number of antennas
    'disable_plot': False,
    'remote_enable': True, # Streaming functionality
    'decode_single_ue': False,
    'rnti': 9185, # single UE decoding
    # RF Config
    'dci_log_config': {
        'lod_dl': True,
        'log_ul': True
    }
}

rf_cfg_tpl = {
    'rf_freq': LibconfInt64(2127500000),
    'N_id_2': -1, 
    'rf_args': 'serial=3272344',
    'nof_thread': 3,
    'disable_plot': True,
    'log_dl': True,
    'log_ul': True,
}

def parseUSRPOutput(output):
    usrps = []
    for line in output.splitlines():
        if 'serial' in line:
            no_spaces = ''.join(line.split())
            usrps.append(no_spaces.split(':')[1])
    return usrps


def getUSRPs():
    try:
        output = subprocess.check_output('uhd_find_devices', shell=True).strip().decode()
    except Exception as e:
        output = ''
    return parseUSRPOutput(output)

def genRFConfig(earfcn, usrpID):
    tmp = rf_cfg_tpl.copy()
    freq = earfcn2freq(earfcn)
    if freq == None:
        print('Invalid EARFCN {0}'.format(earfcn))
        exit(1)
    tmp['rf_freq'] = int(freq*1000000)
    tmp['rf_args'] = 'serial={0}'.format(usrpID)
    
    return tmp

def genConfig(rfNum, earfcns):
    cfg_tpl['nof_rf_dev'] = rfNum
    
    usrps = getUSRPs()
    if len(usrps) < rfNum:
        raise Exception('ERROR: Not enough available USRPs (avail: {0}, req: {1})'.format(len(usrps), rfNum))
    
    # Populate main structure
    cfg_tpl['nof_rf_dev'] = rfNum
    
    # Add RFs
    for i in range(rfNum):
        cfg_tpl['rf_config{0}'.format(i)] = genRFConfig(earfcns, usrps[i])

    # Generate file
    out = dumps(cfg_tpl)
    # Convert booleans into lowercase
    out = out.replace('True', 'true')
    out.replace('False', 'false')

    return out

def safeConfig(cfg, output):
    with open(output, 'w') as f:
        f.write(cfg)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('USAGE: {0} <RF Number> <Earfcn> <Output file>'.format(sys.argv[0]))
        sys.exit(1)
    
    try:
        cfg = genConfig(int(sys.argv[1]), int(sys.argv[2]))
    except Exception as e:
        print(e)
        sys.exit(1)
    
    safeConfig(cfg, sys.argv[3])
    
