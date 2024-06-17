from typing import Dict, Any, Iterator, Optional
from collections import abc
from types import FunctionType
import inspect


class DynamicScope(abc.Mapping):
    #init function basically constructor for class
    def __init__(self):
        self.env: Dict[str, Optional[Any]] = {}
    #get item function returns value from dictionary and catches error and has a try and
    #catch block to stop errors 
    def __getitem__(self, key: str) -> str:
        try:
            return self.env[key]
        except KeyError:
            raise NameError(f"{key} not found in DynamicScope")

    #function to set item in the dictionary 
    def __setitem__(self, key: str, value: str):
        self.env[key] = value
    #function to enable Iteration
    def __iter__(self) ->Iterator:
        return iter(self.env)
    #function to get length
    def __len__(self):
        return len(self.env)
#function to get dynamic variables inspecting the stack and frames to get variables 
#and gather free variables with the list(frame.f_code.co_freevars) line then iterate through for final answer
def get_dynamic_re() -> DynamicScope:
    dynamicscope = DynamicScope()
    stack_info = inspect.stack()

    for frame_info in stack_info:
        frame = frame_info.frame
        free_vars = list(frame.f_code.co_freevars)
        for var_name, var_value in frame.f_locals.items():
            if var_name not in dynamicscope.env and var_name not in free_vars:
                dynamicscope.env[var_name] = var_value
                
    return dynamicscope