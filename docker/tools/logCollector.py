#!/usr/bin/python3

from google.cloud import storage
import sys
import time
import os
import glob
import zipfile
import subprocess
from datetime import datetime

SLEEP_TIME = 20

def pushFileGoogleStorage(local_path, name):
    # https://saturncloud.io/blog/how-to-upload-a-file-to-google-cloud-storage-on-python-3/
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./storage.json"
    client = storage.Client()
    bucket = client.bucket("ng-scope-cosmos")
    blob = bucket.blob(name)
    blob.upload_from_filename(local_path)

def compressFile(file, compressed_file):
    with zipfile.ZipFile(compressed_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(file, arcname=os.path.basename(file))

def fileInUse(path):
    try:
        output = subprocess.check_output('lsof {0}'.format(path), shell=True).strip().decode()
        if 'ngscope' in output:
            return True
        return False  
    except Exception as e:
        return False # lsof returns 1 (error) if the file is not oppened by any process

def main(folder, location, exp_name):
    now = datetime.now()
    date_text = now.strftime("%b_%d_%Y-%H_%M_%S")
    uploaded = set()
    while(True):
        logs = [f for f in glob.iglob('{0}/**/*'.format(folder), recursive=True) if os.path.isfile(f)]
        for log in logs:
            if log in uploaded or fileInUse(log):
                continue
            print('Compressing {0}'.format(log))
            zip_file = os.path.splitext(os.path.basename(log))[0]+'.zip'
            compressFile(log, zip_file)
            if 'sibs' in log:
                storage_path = '{0}/{1}/{2}/sibs/{3}'.format(exp_name, location, date_text, zip_file)
                pushFileGoogleStorage(zip_file, storage_path)
            else:
                storage_path = '{0}/{1}/{2}/dci/{3}'.format(exp_name, location, date_text, zip_file)
                pushFileGoogleStorage(zip_file, storage_path)
            uploaded.add(log)
        time.sleep(SLEEP_TIME)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('USAGE: python3 {0} <Folder> <Location> <experiment_name>'.format(sys.argv[0]))
        exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3])