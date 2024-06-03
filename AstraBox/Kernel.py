from re import T
import tkinter as tk
#from asyncio.windows_events import NULL
import os
import logging
import subprocess
import asyncio
import shutil
import platform

import AstraBox.WorkSpace as WorkSpace
from AstraBox.Models.RunModel import RunModel
import AstraBox.Astra as Astra
import AstraBox.Config as Config
import AstraBox.WSL as WSL

proc = None

current_working_directory = ''

async def run(cmd, logger, stdinput = None):
    global proc
    proc = await asyncio.create_subprocess_exec(
        cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    if stdinput !=None:
        proc.stdin.write(stdinput)    
    #proc.stdin.write(b"1\n1\n1\n1\n1\n")

    while proc.returncode == None:
        data = await proc.stdout.readline()
        line = data.decode('ascii').rstrip()
        if line == '':
            break
        logger.info(line)
        print(proc.returncode)


    # Wait for the subprocess exit.
    await proc.wait()


async def run_shell(cmd, logger):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()


    if stdout:
        logger.info(f'[stdout]\n{stdout.decode("cp866")}')
    if stderr:
        #for line in iter(stderr.readline(),''):
        #    logger.error(line.rstrip())
        logger.error(f'[stderr]\n{stderr.decode("cp866")}')
    print(f'[{cmd!r} exited with {proc.returncode}]')

def log_subprocess_output(pipe, logger):
    for line in iter(pipe.readline, b''): # b'\n'-separated lines
        logger.info('got line from subprocess: %r', line)

async def test_logger(logger):
        logger.info('before sleep')
        await asyncio.sleep(5)
        logger.info('after sleep')
        print('hello')

def isBlank(myString):
    return not (myString and myString.strip())

def isNotBlank(myString):
    return bool(myString and myString.strip())

_logger = None

def get_logger():
    global _logger
    _logger = init_logger('kernel')
    return _logger
    
def init_logger(logger_name):
    logger = logging.getLogger(logger_name)
    while logger.hasHandlers():
        logger.removeHandler(logger.handlers[0])
    logger.setLevel(logging.DEBUG) 
    loc = WorkSpace.get_location_path()
    log_file = os.path.join(loc, f'{logger_name}.log')
    formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt='%H:%M:%S')
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setFormatter(formatter)        
    logger.addHandler(file_handler)
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger

def log_info(info):
    _logger.info(info)

_progress_callback = None
def set_progress_callback(cb):
    global _progress_callback
    WSL._progress_callback = cb
    _progress_callback = cb

def call_progress_callback(progress = 0):
    if _progress_callback:
        _progress_callback(progress)

_astra_profile = None
def set_astra_profile(astra_porfile_name):
    global _astra_profile
    _astra_profile = Config.get_astra_profile(astra_porfile_name)

class Worker:

    def __init__(self, model: RunModel) -> None:
        self.error_flag = False
        self.stdinput = None
        self.run_model = model

    def set_model_status(self, status):
        self.run_model.data['status'] = status
        call_progress_callback()

    def terminate(self):
        self.proc.terminate()
        _logger.info(f'Termitate')
        self.set_model_status('term')

def copy_file(src, dst):
    try:
        shutil.copyfile(src, dst)
        print(f" copy {src} to {dst}")
 
    except shutil.SameFileError:
        print("Source and destination represents the same file.")
 
    except IsADirectoryError:
        print("Destination is a directory.")
 
    except PermissionError:
        print("Permission denied.")
 
    except:
        print(f"Error occurred while copying file: {src} to {dst}")

   

class AstraWorker(Worker):
    def __init__(self, model: RunModel) -> None:
        super().__init__(model)
        WSL._logger = _logger
        _logger.info('create AstraWorker')
        self.wsl_path = f'{_astra_profile["home"]}/{_astra_profile["profile"]}'

    def clear_work_folders(self):
        for key, folder in Astra.data_folder.items():
            clear_cmd = f'rm -f {_astra_profile["profile"]}/{folder}' + '{v*,*.*}'
            WSL.exec(_astra_profile["home"], clear_cmd)

    def copy_data(self):
        zip_file = self.run_model.prepare_run_data()
        WSL.put(zip_file, self.wsl_path)
        WSL.exec(self.wsl_path, f'unzip -o race_data.zip')


    def pack_data(self):
        _logger.info('----- pack data -------')
        WSL.exec(self.wsl_path, f'zip -r race_data.zip dat')
        WSL.exec(self.wsl_path, f'zip -r race_data.zip lhcd')

    def start(self):
        _logger.info(f'start {self.run_model.name}')

        self.clear_work_folders()
        self.copy_data()

        self.set_model_status('run')
        
        astra_cmd = f'./run10.sh {_astra_profile["profile"]} {self.run_model.exp_model.path.name} {self.run_model.equ_model.path.name}'

        WSL.start_exec(_astra_profile["home"],astra_cmd)

        _logger.info('finish')

        self.pack_data()

        zip_path = WorkSpace.get_location_path('RaceModel').joinpath(f'{self.run_model.name}.zip')
        race_zip_file = str(zip_path)
        src = f'{_astra_profile["dest"]}/{_astra_profile["profile"]}/race_data.zip'
        copy_file(src, race_zip_file)
        self.run_model.race_zip_file = race_zip_file

        _logger.info('the end')