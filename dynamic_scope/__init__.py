from typing import Dict, Any, Iterator, Optional
from collections import abc
from types import FunctionType
import inspect


class DynamicScope(abc.Mapping):
    def __init__(self):
        self.env: Dict[str, Optional[Any]] = {}

    def __getitem__(self, key: str) -> str:
        try:
            return self.env[key]
        except KeyError:
            raise NameError(f"{key} not found in DynamicScope")


    def __setitem__(self, key: str, value: str):
        self.env[key] = value

    def __iter__(self) ->Iterator:
        return iter(self.env)

    def __len__(self):
        return len(self.env)

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