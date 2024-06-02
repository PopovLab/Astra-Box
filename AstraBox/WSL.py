import os
import logging
import subprocess
import asyncio
import shutil

def copy_file_to_folder(src, dst):
    try:
        shutil.copy(src, dst)
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

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode("utf-8")}')
    if stderr:
        print(f'[stderr]\n{stderr.decode("utf-8")}')


#wslpath -w /usr/bin
def wslpath(wsl_path):
    pass

def put(local_src, wsl_dst):
    pass



if __name__ == '__main__':
    asyncio.run(run('ls /zzz'))