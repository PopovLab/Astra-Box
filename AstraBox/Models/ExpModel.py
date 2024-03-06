import os
import json
from pathlib import Path
import pyparsing as pp
from AstraBox.Models.BaseModel import RootModel


class Experiment:
    scalars = {}
    vectors = []
    def __init__(self) -> None:
        pass

    def load(self, path) -> None:
        #p = Path(file_name)
        with path.open() as f:
            text = f.readlines()
        self.scalars, self.vectors = self.parsing(text)     



    def parsing(self, text):
        comm1 = pp.AtLineStart(pp.White()) + pp.rest_of_line
        comm2 = pp.AtLineStart(pp.Literal('!')) + pp.rest_of_line
        comments = comm1 | comm2 
        #POINTS   81    GRIDTYPE 1    NAMEXP TIX    NTIMES 1
        word = pp.Word(pp.printables)
        var_name = pp.Word(init_chars= pp.alphas, body_chars= pp.alphanums)
        tag = pp.one_of(['POINTS', 'GRIDTYPE', 'NAMEXP', 'NTIMES', 'FACTOR'])
        vector_header = pp.OneOrMore( pp.Group(tag + word))('vector')
        
        record = pp.Group(var_name("var") + pp.OneOrMore(pp.pyparsing_common.fnumber )('value')).set_results_name('scalar')
        value = pp.pyparsing_common.sci_real | pp.pyparsing_common.integer
        value_array = pp.OneOrMore(value).set_results_name('data')
        record.ignore(pp.AtLineStart('!') + pp.rest_of_line)
        #test = pp.Suppress(comments) | vector_header | record | value_array
        test = vector_header | record | value_array

        scalar_vars = {}
        vectors = []
        new_vector = None
        #print('-------------')
        scalar_flag = True
        for t in text:
            if t.startswith('END'):
                break
            if t.startswith('!'):
                #print(f'comment: {t}')
                continue
            if t.isspace():
                #print('is space')
                continue    
            if scalar_flag and t.startswith(' '):
                #print(f'comment: {t}')
                continue
            try:
                print(t)
                res = test.parseString(t)
                #print(res.dump())
                if 'scalar' in res :
                    #print(f'{res.scalar.var} = {res.scalar.value}')
                    if res.scalar.var in scalar_vars:
                        scalar_vars[res.scalar.var].append(res.scalar.value.as_list())
                    else:
                        scalar_vars[res.scalar.var] = [res.scalar.value.as_list()]
                else: 
                    if 'vector' in res:
                        #print(f' {res.vector}')
                        new_vector = {'data' : []}
                        for p in res.vector.as_list():
                            new_vector[p[0]] = p[1]

                        vectors.append(new_vector)
                        scalar_flag = False
                    if 'data' in res:
                        new_vector['data'].append(res.data.as_list())
                    else:
                        pass
                        #print(res.dump())
            except Exception as ex: 
                print(t)
                print(ex)    
    
        for key, v in scalar_vars.items():
            if len(v) == 1:
                if len(v[0]) == 1:
                    scalar_vars[key] = v[0][0]            
        return scalar_vars, vectors        

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