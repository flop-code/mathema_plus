from collections import OrderedDict
from collections.abc import Mapping
from dataclasses import dataclass
from math import ceil
from typing import Annotated, TypeAlias

import hyperdiv as hd


FormulaType: TypeAlias = Annotated[str, "formula"]
VariableNameType: TypeAlias = Annotated[str, "variable name"]
VariableValueType: TypeAlias = Annotated[float, "variable value"]


@dataclass
class Interval:
    start: float
    stop: float
    
    @property
    def float_tuple(self) -> tuple[float, float]:
        return (self.start, self.stop)

    @property
    def int_tuple(self) -> tuple[int, int]:
        return (ceil(self.start), ceil(self.stop))
    
    def contains(self, value: float) -> bool:
        return self.start <= value <= self.stop


@dataclass
class VariableProperties:
    interval: Interval
    is_proper_fraction: bool
    is_decimal_fraction: bool


class Solution(Mapping):
    """Immutable and hashable mapping of variables to their values."""

    def __init__(self, *solution_dictionary: Mapping[VariableNameType, VariableValueType]):
        self.__dict = {k: v for d in solution_dictionary for k, v in d.items()}

    def __iter__(self):
        return iter(self.__dict)

    def __len__(self):
        return len(self.__dict)

    def __getitem__(self, key):
        return self.__dict[key]

    def __hash__(self):
        return hash(tuple(sorted((k, round(v, 10)) for k, v in self.items())))


@hd.global_state
class GenerationTask(hd.task):
    """Global cancelable task to control the generation process."""

    _canceled: bool = hd.Prop(hd.Any, False)

    @property
    def canceled(self) -> bool:
        return self._canceled
    
    def cancel(self) -> None:
        self._canceled = True

    def clear(self, *args, **kwargs) -> None:
        self.cancel()
        super().clear(*args, **kwargs)
    
    def run(self, *args, **kwargs) -> None:
        self._canceled = False
        super().run(*args, **kwargs)
