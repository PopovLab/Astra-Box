import os
import json
from pathlib import Path
import pyparsing as pp
from AstraBox.Models.RootModel import RootModel


class Experiment:
    scalars = {}
    vectors = []
    def __init__(self) -> None:
        pass

    def load(self, path) -> None:
        #p = Path(file_name)
        with path.open() as f:
            text = f.readlines()
        self.scalars, self.grid_vars = self.parsing(text)     

    def parsing(self, text):
        comm1 = pp.AtLineStart(pp.White()) + pp.rest_of_line
        comm2 = pp.AtLineStart(pp.Literal('!')) + pp.rest_of_line
        comments = comm1 | comm2 
        #POINTS   81    GRIDTYPE 1    NAMEXP TIX    NTIMES 1
        word = pp.Word(pp.printables)
        var_name = pp.Word(init_chars= pp.alphas, body_chars= pp.alphanums)
        tag = pp.one_of(['POINTS', 'GRIDTYPE', 'NAMEXP', 'NTIMES', 'FACTOR'])
        grid_header = pp.OneOrMore( pp.Group(tag + word))('grid_header')
        
        record = pp.Group(var_name("var") + pp.OneOrMore(pp.pyparsing_common.fnumber )('value')).set_results_name('scalar')
        value = pp.pyparsing_common.sci_real | pp.pyparsing_common.integer
        value_array = pp.OneOrMore(value).set_results_name('data')
        record.ignore(pp.AtLineStart('!') + pp.rest_of_line)
        #test = pp.Suppress(comments) | vector_header | record | value_array
        test = grid_header | record | value_array

        exp_vars = {}
        grid_vars = {}
        grid = None

        for t in text:
            if t.startswith('END'):
                break
            if t.startswith('!'):
                #print(f'comment: {t}')
                continue
            if t.isspace():
                #print('is space')
                continue    
            if t.startswith(' '):
                #print(f'comment: {t}')
                continue
            try:
                #print('-------------')
                #print(t)
                res = test.parseString(t)
                #print(res.dump())
                match res:
                    case _ if 'scalar' in res :
                        #print(f'{res.scalar.var} = {res.scalar.value}')
                        if res.scalar.var in exp_vars:
                            exp_vars[res.scalar.var].append(res.scalar.value)
                        else:
                            exp_vars[res.scalar.var] = [res.scalar.value]
                    case _ if 'grid_header' in res:
                        #print(res.dump())
                        grid = {k: int(v) if v.isdigit() else v for k, v in res.grid_header}
                        #print(grid)
                        grid['data'] = []
                        grid_vars[grid['NAMEXP']] = grid
                    case _ if 'data' in res:
                        #print(res.dump())
                        if grid:
                            grid['data'].append(res.data.as_list())
                    case _ :
                        pass
                        #print(res.dump())
            except Exception as ex: 
                print(t)
                print(ex)    
    
        for key, v in exp_vars.items():
            if len(v) == 1:
                exp_vars[key] = v[0]   
        #for key, v in grid_vars.items():    
        #    print(v['NAMEXP'])
        #    for x in v['data']:
        #        print(x)
        return exp_vars, grid_vars        

    def print_scalars(self):
        print('scalars data:')
        for key, v in self.scalars.items():
            print(f'{key}: {v}')


class ExpModel(RootModel):

    def __init__(self, name= None, path= None) -> None:
        if name:
            super().__init__(name)
        if path:
            super().__init__(path.stem)
            self.path = path
        self._setting = None
        self.changed = False
        self.experiment = None


    @property
    def model_kind(self):
        return 'ExpModel'


    def get_dest_path(self):
        return os.path.join('exp', self.path.name)
    

    def get_experiment(self):
        if self.experiment is None:
            #fn = self.get_dest_path()
            self.experiment = Experiment()
            self.experiment.load(self.path)
        return self.experiment