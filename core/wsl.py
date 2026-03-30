import asyncio

from AstraBox import Astra

# replacement strings
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'
# Windows ➡ Unix
#content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
# Unix ➡ Windows
# content = content.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING)


def create_runner(log):
    return WSLRunner(log)

async def progress_run(cmd, log):
    process  = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    # Create tasks to read stdout and stderr streams
    async def read_stream(stream, prefix=''):
        """Read lines from a stream and print them"""
        while True:
            data = await stream.readline()
            if not data:
                break
            data = data.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING)
            line = data.decode('ascii').rstrip()
            if prefix == 'ERROR':
                log.error(line)
            else:
                log.info(line)
    
    # Create tasks for stdout and stderr
    stdout_task = asyncio.create_task(read_stream(process.stdout))
    stderr_task = asyncio.create_task(read_stream(process.stderr, 'ERROR'))
    
    # Wait for both reading tasks to complete
    await asyncio.wait([stdout_task, stderr_task])
    
    # Wait for the process to finish
    return_code = await process.wait()
    return return_code 

class WSLRunner():
    def __init__(self, log) -> None:
        self.log = log
        self.log.info('create WSLRunner')

    def check_astra_profile(self, astra_profile)-> bool:
        astra_user = astra_profile["profile"]
        astra_home = astra_profile["home"]
        print('check dir')
        print(astra_home)
        return self.check_dir(astra_home)
    
    def check_dir(self, wsl_folder):
        ps_cmd = f'wsl bash {wsl_folder}'
        self.log.info(f'check: {wsl_folder}')
        return asyncio.run(self.checked_run(ps_cmd))

    async def checked_run(self, cmd)->bool:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)

        stdout, stderr = await proc.communicate()

        print(f'[{cmd!r} exited with {proc.returncode}]')
        lines = stdout.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING).decode('ascii').split("\r\n")
        for line in lines:
            self.log.info(line)

        lines = stderr.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING).decode('ascii').split("\r\n")
        for line in lines:
            self.log.info(line)

        if (proc.returncode == 0) or (proc.returncode == 126):
            return True #stdout.removesuffix(UNIX_LINE_ENDING).decode(get_CP())
        else:
            return False
    
    def exec(self, wsl_work_folder, command):
        ps_cmd = f'wsl --cd {wsl_work_folder} {command}'
        self.log.info(f'exec: {wsl_work_folder} {command}')
        asyncio.run(progress_run(ps_cmd, self.log))

    def clear_work_folders(self, astra_home, astra_user):
        for key, folder in Astra.data_folder.items():
            clear_cmd = f'rm -f {astra_user}/{folder}' + '{v*,*.*}'
            self.exec(astra_home, clear_cmd)
        clear_cmd = f'rm -f {astra_user}/' + '*.mod'
        self.exec(astra_home, clear_cmd)
        clear_cmd = f'rm -f {astra_user}/sbr/' + '*.f90'
        self.exec(astra_home, clear_cmd)   