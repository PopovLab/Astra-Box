from typing import Literal
from pydantic import BaseModel, Field

class SubPlot(BaseModel):
    name: str
    title: str = ''
    data: list[str]

class PlotSetting(BaseModel):
    title: str
    show_grid: bool = True
    shape: str
    x_axis: str 
    x_axis_list : list[str] = Field(default=[], exclude=True)
    sub_plots: list[SubPlot]
    
    data_terms: list[str] = Field(default=[], exclude=True)

    def get_sub_plots_names(self):
        return [x.name for x in self.sub_plots]
    
    def get_sub_plot(self, name: str):
        return [x for x in self.sub_plots if x.name == name][0]