import os
import logging
import subprocess
import sys
import asyncio
import shutil
from ctypes import windll
import subprocess

def GetConsoleOutputCP():
    'Get Console Output CP '
    cp= windll.kernel32.GetConsoleOutputCP()
    return f"CP{cp}"

__CP = None


def get_CP():
    global __CP
    if __CP is None:
        __CP = GetConsoleOutputCP()
    return __CP

def copy_file_to_folder(src, dst):
    try:
        res = shutil.copy(src, dst)
        print(res)
        print(f" copy {src} to {dst}")
 
    except shutil.SameFileError:
        print("Source and destination represents the same file.")
 
    except IsADirectoryError:
        print("Destination is a directory.")
 
    except PermissionError:
        print("Permission denied.")
 
    except:
        print(f"Error occurred while copying file: {src} to {dst}")

remotepath = '/path/to/remote/file.py'
localpath = '/path/to/local/file.py'
# replacement strings
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'
# Windows ➡ Unix
#content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
# Unix ➡ Windows
# content = content.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING)

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')

    if proc.returncode == 0:
        return stdout.removesuffix(UNIX_LINE_ENDING).decode(get_CP())
    else:
        return None
    
_progress_callback = None

def progress(progress = 0):
    if _progress_callback:
        _progress_callback(progress)

_logger = None

def log_info(msg):
    if _logger:
        _logger.info(msg)

def exec(wsl_work_folder, command):
    ps_cmd = f'wsl --cd {wsl_work_folder} {command}'
    log_info(f'exec: {command}')
    out=  asyncio.run(run(ps_cmd))
    log_info(out)
#wslpath -w /usr/bin

def win_wsl_path(wsl_path):
    cmd = f'wsl wslpath -w {wsl_path}'
    return asyncio.run(run(cmd))

def put(local_src, wsl_dst):
    log_info(f'copy : {local_src}')
    log_info(f'to: {wsl_dst}')
    win_wsl_dst = win_wsl_path(wsl_dst)
    copy_file_to_folder(local_src, win_wsl_dst)


if __name__ == '__main__':
    print(GetConsoleOutputCP())
    print(sys.getdefaultencoding())
    asyncio.run(run('wsl ls /zzz'))
    
    wp = win_wsl_path('/home/tmp8')
    print(wp)
    put("d:\spcpz.dat",'/home/tmp8/ASTRA-6/a4')