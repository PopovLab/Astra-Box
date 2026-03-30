import asyncio

# replacement strings
WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'
# Windows ➡ Unix
#content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)
# Unix ➡ Windows
# content = content.replace(UNIX_LINE_ENDING, WINDOWS_LINE_ENDING)


def create_runner(log):
    return WSLRunner(log)


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