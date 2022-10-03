from re import T
import tkinter as tk
from asyncio.windows_events import NULL
import os
import logging
import subprocess
import asyncio
import Utils
from Models import ImpedModel

proc = NULL

current_working_directory = None

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


async def run_shel(cmd, logger):
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


class Worker:


    def get_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        while logger.hasHandlers():
            logger.removeHandler(logger.handlers[0])
        logger.setLevel(logging.DEBUG) 
        log_file = os.path.join(self.work_folder, f'{logger_name}.log')
        formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt='%H:%M:%S')
        file_handler = logging.FileHandler(log_file, mode='w')
        file_handler.setFormatter(formatter)        
        logger.addHandler(file_handler)
        # with this pattern, it's rarely necessary to propagate the error up to parent
        logger.propagate = False
        return logger

    on_progress = None
    controller = None

    def __init__(self, model) -> None:
        self.stdinput = None
        self.model = model
        self.work_folder = self.model.get_work_folder()
        self.logger = self.get_logger('kernel')
        self.logger.info( type(self)) 
        self.logger.log(logging.INFO, 'folder: ' + self.work_folder) 

    def set_model_status(self, status):
        self.model.data['status'] = status
        if self.controller:
            self.controller.update_model_status(self.model)

    async def run(self, cmd):
        self.error_flag = False
        self.logger.log(logging.INFO, f"run_cmd: {self.run_cmd}")
        os.chdir(self.work_folder)
        self.logger.log(logging.INFO, f"CWD: {os.getcwd()}")
        self.proc = await asyncio.create_subprocess_exec(
            cmd,
            #universal_newlines= True,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        if self.stdinput !=None:
            self.proc.stdin.write(self.stdinput)    
        #self.proc.stdin.write(b"1\n1\n1\n1\n1\n")

        while self.proc.returncode == None:
            data = await self.proc.stdout.readline()
            line = data.decode('ascii').rstrip()

            if self.proc.stdout.at_eof(): break
            if self.on_progress:
                self.on_progress(2)
                
            if line.startswith(' done'):
                progress = float(line[10:])
                if self.on_progress:
                    self.on_progress(progress)
                continue
            if 'FATAL ERROR' in line:
                self.error_flag = True
            self.logger.info(line)

        stdout, stderr = await self.proc.communicate()
        lines = stdout.decode('ascii').split("\r\n")
        for line in lines:
            self.logger.info(line)

        lines = stderr.decode('ascii').split("\r\n")
        for line in lines:
            self.logger.error(line)

 

    def terminate(self):
        self.proc.terminate()
        self.logger.info(f'Termitate')
        self.set_model_status('term')
