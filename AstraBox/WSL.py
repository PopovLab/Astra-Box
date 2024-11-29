import os
import logging
import subprocess
import sys
import asyncio
import shutil

import subprocess
import platform

match platform.system():
    case 'Windows':
        from ctypes import windll
    case 'Darwin':
        print('Darwin')

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


# replacement strings
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'
# Windows ➡ Unix
#content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
# Unix ➡ Windows
# content = content.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING)

#wslpath -w /usr/bin

def win_wsl_path(wsl_path):
    cmd = f'wsl wslpath -w {wsl_path}'
    return asyncio.run(run(cmd))

def put(local_src, wsl_dst):
    log_info(f'copy : {local_src}')
    log_info(f'to: {wsl_dst}')
    win_wsl_dst = win_wsl_path(wsl_dst)
    copy_file_to_folder(local_src, win_wsl_dst)

def get(wsl_src, local_dst):
    log_info(f'copy : {wsl_src}')
    log_info(f'to: {local_dst}')
    win_wsl_src = win_wsl_path(wsl_src)
    copy_file(win_wsl_src, local_dst)

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


async def checked_run(cmd)->bool:
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    lines = stdout.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING).decode('ascii').split("\r\n")
    for line in lines:
        log_info(line)

    lines = stderr.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING).decode('ascii').split("\r\n")
    for line in lines:
        log_error(line)

    if (proc.returncode == 0) or (proc.returncode == 126):
        return True #stdout.removesuffix(UNIX_LINE_ENDING).decode(get_CP())
    else:
        return False

_progress_callback = None

def progress(progress = 0):
    if _progress_callback:
        _progress_callback(progress)

async def progress_run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    while proc.returncode == None:
        data = await proc.stdout.readline()
        data = data.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING)
        line = data.decode('ascii').rstrip()
        if proc.stdout.at_eof(): break
        progress()
        log_info(line)

    stdout, stderr = await proc.communicate()
    lines = stdout.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING).decode('cp866').split("\r\n")
    for line in lines:
        log_info(line)

    #print(stderr)
    #print(sys.stdout.encoding)
    #print('---------------------')
    #lines = stderr.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING).decode('utf-8', errors='ignore').split("\r\n")
    lines = stderr.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING).decode('cp866').split("\r\n")
    for line in lines:
        log_error(line)

_logger = None

def isNotBlank(myString):
    return bool(myString and myString.strip())

def log_info(msg):
    if _logger:
        if isNotBlank(msg):
            _logger.info(msg)

def log_error(msg):
    if _logger:
        if isNotBlank(msg):
            _logger.error(msg)            

def start_exec(wsl_work_folder, command):
    ps_cmd = f'start wsl --cd {wsl_work_folder} {command}'
    log_info(f'exec: {command}')
    asyncio.run(progress_run(ps_cmd))


def exec_command(wsl_work_folder, command):
    ps_cmd = f"wsl --cd {wsl_work_folder} -e bash -c '{command}'"
    print(ps_cmd)
    log_info(f'exec: {ps_cmd}')
    asyncio.run(progress_run(ps_cmd))

def exec(wsl_work_folder, command):
    ps_cmd = f'wsl --cd {wsl_work_folder} {command}'
    log_info(f'exec: {wsl_work_folder} {command}')
    asyncio.run(progress_run(ps_cmd))

def check_dir(wsl_folder):
    ps_cmd = f'wsl bash {wsl_folder}'
    log_info(f'check: {wsl_folder}')
    return asyncio.run(checked_run(ps_cmd))



if __name__ == '__main__':
    print(GetConsoleOutputCP())
    print(sys.getdefaultencoding())
    asyncio.run(run('wsl ls /zzz'))
    
    wp = win_wsl_path('/home/tmp8')
    print(wp)
    put("d:\spcpz.dat",'/home/tmp8/ASTRA-6/a4')