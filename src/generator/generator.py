from typing import Any
from generator import _generator_builtins
from generator.types import *

from fractions import Fraction
from random import randint, uniform
from typing import Iterable
from time import time


def _generate_value(properties: VariableProperties) -> VariableValueType | None:
    """Generate a value for a variable based on its properties.
    Returns None if the random value generation failed.
    """

    if properties.interval.start >= properties.interval.stop:
        return None

    value = float("inf")

    if properties.is_proper_fraction:
        denominator = randint(2, 5)

        numerator = randint(
            int(properties.interval.start * denominator),
            int(properties.interval.stop * denominator)
        )

        fraction = Fraction(numerator, denominator)

        if fraction.denominator == 1:
            return None

        value = float(fraction)
    elif properties.is_decimal_fraction:
        random_value = uniform(*properties.interval.float_tuple)

        value = round(random_value, randint(2, 2))
        
        if value.is_integer():
            return None
    else:
        value = randint(*properties.interval.int_tuple)

    if properties.interval.contains(value):
        return value
    return None


def evaluate(
    formula: FormulaType,
    values: Mapping[VariableNameType, VariableValueType]
) -> Any:
    """Evaluate a formula (Python expression) with the given values.
    Returns the result of the evaluation or False if an exception occurs.
    """
    try:
        evaluation = eval(formula, _generator_builtins.__dict__, values)
        if isinstance(evaluation, complex):
            return float("-inf")
        return evaluation
    except Exception as e:
        print("Log (OK):", formula, e, flush=True)
        return float("-inf")


def _is_solution(
    values: Mapping[VariableNameType, VariableValueType],
    conditions: Iterable[FormulaType]
) -> bool:
    """Check if the given values satisfy all the given conditions."""

    return all(evaluate(cond, values) for cond in conditions)


def generate_solutions(
    variables: Mapping[VariableNameType, VariableProperties],
    conditions: Iterable[FormulaType],
    num_of_solutions: int,
    generator_location: str,
    max_attempts_per_solution: int = 50_000
) -> set[Solution] | None:
    """Generate solutions for the given variables and conditions.
    Returns a set of solutions, or None if there are not enough solutions
    generated within the given number of attempts, or empty set if the
    generation task was canceled.
    """

    solutions: set[Solution] = set()
    start_time = time()
    generation_task = GenerationTask()

    for _ in range(max_attempts_per_solution * num_of_solutions):
        if generation_task.canceled or hd.location().path != generator_location:
            return set()
        if time() - start_time > 60:
            return None

        values: dict[VariableNameType, VariableValueType] = {}

        for var, properties in variables.items():
            value = _generate_value(properties)
            if value is None:
                break

            values[var] = value
        else:
            if _is_solution(values, conditions):
                solutions.add(Solution(values))
            if len(solutions) == num_of_solutions:
                break
    else:
        return None

    return solutions
