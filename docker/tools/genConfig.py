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
        'log_ul': True,
        'log_interval': 200,
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
    lines = output.splitlines()

    indexes = []
    for i, line in enumerate(lines):
        if 'Device Address:' in line:
            indexes.append(i)
    indexes.append(-1)
    
    for i in range(len(indexes)-1):
        start = indexes[i]
        end = indexes[i+1]
        args = ''
        for line in lines[start:end]:
            if 'serial' in line:
                if args != '':
                    args += ','
                args += ''.join(line.split()).replace(':', '=')
            if 'addr' in line:
                if args != '':
                    args += ','
                args += ''.join(line.split()).replace(':', '=')
        usrps.append(args)

    return usrps


def getUSRPs():
    try:
        output = subprocess.check_output('uhd_find_devices', shell=True).strip().decode()
    except Exception as e:
        output = ''
    return parseUSRPOutput(output) # List of USRPs in the system

def genRFConfig(earfcn, usrpArgs):
    tmp = rf_cfg_tpl.copy()
    freq = earfcn2freq(int(earfcn))
    if freq == None:
        print('Invalid EARFCN {0}'.format(earfcn))
        exit(1)
    tmp['rf_freq'] = int(freq*1000000)
    tmp['rf_args'] = usrpArgs
    
    return tmp

def genConfig(frag, earfcns):    
    usrps = getUSRPs()
    if len(usrps) < len(earfcns):
        raise Exception('ERROR: Not enough available USRPs (avail: {0}, req: {1})'.format(len(usrps), len(earfcns)))
    
    # Populate main structure
    cfg_tpl['nof_rf_dev'] = len(earfcns)
    cfg_tpl['dci_log_config']['log_interval'] = int(frag)
    
    # Add RFs
    for i in range(len(earfcns)):
        cfg_tpl['rf_config{0}'.format(i)] = genRFConfig(earfcns[i], usrps[i])

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
    if len(sys.argv) < 4:
        print('USAGE: {0} <Fragmentation> <Output file> <Earfcn List>'.format(sys.argv[0]))
        sys.exit(1)
    
    try:
        cfg = genConfig(sys.argv[1], sys.argv[3:])
    except Exception as e:
        print(e)
        sys.exit(1)
    
    safeConfig(cfg, sys.argv[2])