from re import T
import tkinter as tk
#from asyncio.windows_events import NULL
import os
import logging
import subprocess
import asyncio
import shutil
import platform

from AstraBox.Models import ModelFactory
from AstraBox.Task import Task
import AstraBox.WorkSpace as WorkSpace
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

#_astra_profile = None
#def set_astra_profile(astra_porfile_name):
#    global _astra_profile
#    _astra_profile = Config.get_astra_profile(astra_porfile_name)

class Worker:
    def __init__(self) -> None:
        self.error_flag = False
        self.stdinput = None

    def set_model_status(self, status):
        #self.run_model.data['status'] = status
        call_progress_callback()

    def terminate(self):
        self.proc.terminate()
        _logger.info(f'Termitate')
        self.set_model_status('term')


class AstraWorker(Worker):
    def __init__(self) -> None:
        super().__init__()
        _logger.info('create AstraWorker')

    def mk_work_folders(self):
        for key, folder in Astra.basic_folder.items():
            mk_cmd = f'mkdir {self.astra_user}/{folder}'
            WSL.exec(self.astra_home, mk_cmd)

    def clear_work_folders(self):
        for key, folder in Astra.data_folder.items():
            clear_cmd = f'rm -f {self.astra_user}/{folder}' + '{v*,*.*}'
            WSL.exec(self.astra_home, clear_cmd)
        clear_cmd = f'rm -f {self.astra_user}/' + '*.mod'
        WSL.exec(self.astra_home, clear_cmd)
        clear_cmd = f'rm -f {self.astra_user}/sbr/' + '*.f90'
        WSL.exec(self.astra_home, clear_cmd)        

    def copy_data(self, task: Task):
        #zip_file = self.run_model.prepare_run_data()
        zip_file= WorkSpace.get_location_path().joinpath('race_data.zip')
        errors = ModelFactory.prepare_task_zip(task, zip_file)
        if len(errors)>0:
            for e in errors:
                _logger.error(e)
            _logger.error('запуск не возможен из-за ошибок')
            return True
        WSL.put(zip_file, self.wsl_path)
        WSL.exec(self.wsl_path, f'unzip -o race_data.zip')
        return False


    def pack_data(self):
        _logger.info('----- pack data -------')
        WSL.exec(self.wsl_path, f'zip -r race_data.zip dat')
        WSL.exec(self.wsl_path, f'zip -r race_data.zip lhcd')

    def pack_task_results(self, task:Task):
        _logger.info(f'----- pack task results {task.index} -------')
        print(f'----- pack task results {task.index} -------')
        task_folder = f'task_{task.index}'
        WSL.exec(self.wsl_path, f'mkdir {task_folder}')
        WSL.exec(self.wsl_path, f'mv dat {task_folder}')
        WSL.exec(self.wsl_path, f'mkdir {task_folder}/equ')       
        WSL.exec(self.wsl_path, f'cp equ/{task.equ} {task_folder}/equ')
        WSL.exec(self.wsl_path, f'mkdir {task_folder}/exp')       
        WSL.exec(self.wsl_path, f'cp exp/{task.exp} {task_folder}/exp')        
        #WSL.exec(self.wsl_path, f'mv lhcd {task_name}')
        WSL.exec(self.wsl_path, f'zip -r race_data.zip {task_folder}')
        WSL.exec(self.wsl_path, f'rm -r {task_folder}')

    def sub_task_generaton(self, task: Task):
        folder = WorkSpace.folder('ExpModel')
        for index, (name, folder_item) in enumerate(folder.generator(task.exp)):
            #exp_model = load(folder_item)
            sub_task = Task(exp=name, equ=task.equ, frtc=task.frtc, spectrum=task.spectrum)
            sub_task.index = index
            yield sub_task

    def execute(self, task: Task,  option:str='no_pause'):
        astra_profile = Config.get_astra_profile(task.astra_profile)
        print(astra_profile)
        if not check_astra_profile(astra_profile):
            WSL.log_error('нет Астры')
            return
        self.astra_user = astra_profile["profile"]
        self.astra_home = astra_profile["home"]

        self.wsl_path = f'{self.astra_home}/{self.astra_user}'
        _logger.info(f'start {task.name}')

        self.clear_work_folders()
        
        if self.copy_data(task):  return

        self.set_model_status('run')
        if task.exp == '*.*':
            for sub_task in self.sub_task_generaton(task):
                astra_cmd = f'./run_astra.sh {self.astra_user} {sub_task.exp} {sub_task.equ} {option}'
                print(sub_task)
                WSL.start_exec(self.astra_home, astra_cmd)
                self.pack_task_results(sub_task)
                self.mk_work_folders()
        else:

            astra_cmd = f'./run_astra.sh {self.astra_user} {task.exp} {task.equ} {option}'
            WSL.start_exec(self.astra_home, astra_cmd)
            self.pack_data()

        _logger.info('finish')

        
        
        
        zip_path = WorkSpace.get_path('RaceModel').joinpath(f'{task.name}.zip')
        race_zip_file = str(zip_path)
        src = f'{self.astra_home}/{self.astra_user}/race_data.zip'
        WSL.get(src, race_zip_file)
        #self.run_model.race_zip_file = race_zip_file

        _logger.info('the end')

def check_astra_profile(astra_profile)-> bool:
    astra_user = astra_profile["profile"]
    astra_home = astra_profile["home"]
    print('check dir')
    print(astra_home)
    
    return WSL.check_dir(astra_home)

def execute(task: Task, option:str):
    WSL._logger = _logger
    worker = AstraWorker()
    worker.execute(task, option)



