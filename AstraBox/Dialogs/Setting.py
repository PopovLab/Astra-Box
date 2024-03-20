from typing import Literal
from pydantic import BaseModel, Field

import AstraBox.WorkSpace as WorkSpace

class SubPlot(BaseModel):
    name: str
    title: str = ''
    y_label: str = Field(default='Value [arb. unit]')
    data: list[str]

class PlotSetting(BaseModel):
    title: str
    show_grid: bool = True
    shape: str
    x_axis: str 
    x_axis_list : list[str] = Field(default=[], exclude=True)
    x_label: str = Field(default='Value [arb. unit]')
    sub_plots: list[SubPlot]
    
    data_terms: list[str] = Field(default=[], exclude=True)

    def get_sub_plots_names(self):
        return [x.name for x in self.sub_plots]
    
    def get_sub_plot(self, name: str):
        return [x for x in self.sub_plots if x.name == name][0]
    
    @classmethod
    def load(cls, fn:str):
        loc = WorkSpace.get_location_path().joinpath(fn)
        if loc.exists():
            with open(loc) as file:
                data = file.read()
            return cls.model_validate_json(data)
        else:
            return None

    def save(self, fn:str):
        loc = WorkSpace.get_location_path().joinpath(fn)
        with open(loc, "w" ) as file:
            file.write(self.model_dump_json(indent= 2))

