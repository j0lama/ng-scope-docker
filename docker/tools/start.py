import os
import signal
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import subprocess as sp
from time import sleep

import genConfig as gc

def parse_timeout(timestr=None):
    if timestr is not None:
        timestr = timestr.lower()
        if timestr[-1] == 'h':
            return float(timestr[:-1]) * 3600
        elif timestr[-1] == 'm':
            return float(timestr[:-1]) * 60
        elif timestr[-1] == 's':
            return float(timestr[:-1])
        else:
            return float(timestr)
    else:
        return None

def kill_docker(p: sp.Popen):
    p.stdin.write(b'\x03')
    p.stdin.flush()
    p.wait()

def main():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-e', '--earfcns', type=int, nargs='*', help='List of EARFCNs')
    parser.add_argument('-d', '--directory', default=os.curdir, help='Output directory')
    parser.add_argument('-i', '--image', default='j0lama/ng-scope', help='Docker image to run')
    parser.add_argument('-t', '--timeout')
    parser.add_argument('-f', '--fragment', type=int, default=0)
    parser.add_argument('-c', '--config', default='config.cfg')
    parser.add_argument('-l', '--logs', default='./logs/logs')
    args = parser.parse_args()

    timeout = parse_timeout(args.timeout)
    if timeout == 0:
        timeout = None
    directory = os.path.abspath(args.directory)
    os.makedirs(directory, exist_ok=True)

    for i, earfcn in enumerate(args.earfcns):
        gc.generate_and_write(args.fragment, args.config, [earfcn])
        sib_logs = os.path.join(args.logs, 'sibs')
        dci_logs = os.path.join(args.logs, 'dci_output')
        cmd = f'./ngscope -c {args.config} -s {sib_logs} -o {dci_logs}'
        p = sp.Popen(cmd, shell=True, stdin=sp.PIPE)
        try:
            p.wait(timeout)
        except KeyboardInterrupt:
            p.wait()
        except sp.TimeoutExpired:
            # sp.run(f'kill {p.pid}', shell=True)
            # p.wait()
            # kill_docker(p)
            # p.terminate()
            # p.send_signal(signal.SIGINT)
            p.kill()
            p.wait()
        if i < len(args.earfcns) - 1:
            sleep(10)

if __name__ == '__main__':
    main()
