

def create_runner(log):
    return WSLRunner(log)

class WSLRunner():
    def __init__(self, log) -> None:
        self.log = log
        self.log.info('create WSLRunner')