import pathlib
from datetime import datetime
from typing import Literal
from typing import List, Optional
from pydantic import BaseModel, Field

def datetime_now() -> str:
    print(datetime.now())
    return datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

class Task(BaseModel):
    index: int = Field(default=0, exclude=True)
    name:  str = Field(default_factory=datetime_now)
    title: str = 'Task'
    exp:   str = ''
    equ:   str = ''
    rt: Optional[str] = None
    frtc: Optional[str] = None
    spectrum: Optional[str] = None
    astra_profile: str = ''

    @classmethod
    def load(cls, data):
        try:
            return cls.model_validate_json(data)
        except:
            return cls.model_validate_json('{}')


    @classmethod
    def load_from_file(cls, path:str):
        loc = pathlib.Path(path)
        if loc.exists():
            with open(loc) as file:
                data = file.read()
            return cls.model_validate_json(data)
        else:
            return cls.model_validate_json('{}')

    def dump(self):
        return self.model_dump_json(indent= 2)
    
    def save(self, path:str):
        loc = pathlib.Path(path)
        with open(loc, "w" ) as file:
            file.write(self.model_dump_json(indent= 2))    

class TaskList(BaseModel):
    main_task: Task
    tasks: list[Task] = Field(default= [])



if __name__ == '__main__':
    task1 = Task(exp='21', equ='22')
    print(task1)
    task2 = Task.load_from_file('task1.tsk')
    for name, value in task2:
        if not value is None:
            print(f'{name}: {value}')


    #test_rtp(rtp, 'test_rtp.txt')