from generator.types import Solution, VariableNameType, VariableValueType

from io import BytesIO
from functools import lru_cache
from fractions import Fraction
from typing import (
    Callable,
    Protocol,
    Sequence,
    Iterable,
    TypeAlias,
    Literal,
    Mapping
)

import hyperdiv as hd
import matplotlib
import matplotlib.pyplot as plt


matplotlib.use("Agg")
plt.rc("mathtext", fontset="cm")


class TexImageGenerator(Protocol):
    def __call__(self, tex_formula: str, pad_inches: float = 0.0) -> bytes: ...


def tex_image(tex_formula: str, pad_inches: float = 0.0) -> bytes:
    fig = plt.figure(dpi=650)
    
    color = "black" if hd.theme().is_light else "white"
    fig.text(0, 0, f"${tex_formula}$", ha="center", va="center", color=color)

    output = BytesIO()

    fig.savefig(
        output, transparent=True, format="png",
        bbox_inches='tight', pad_inches=pad_inches
    )

    output.seek(0)
    img = output.getvalue()

    output.close()
    plt.close(fig)

    return img


def get_cached_image_generator() -> TexImageGenerator:
    @lru_cache
    def cached_image_generator(is_light_theme: bool, *args, **kwargs) -> bytes:
        return tex_image(*args, **kwargs)

    def wrapper(*args, **kwargs) -> bytes:
        return cached_image_generator(hd.theme().is_light, *args, **kwargs)

    return wrapper


def float_to_tex_proper_fraction(number: float) -> str:
    fraction = Fraction(number).limit_denominator(100)

    if fraction.denominator == 1:
        return str(int(number))

    return (
        ("-" if fraction.numerator < 0 else "")
        + r"\frac{"
        + str(abs(fraction.numerator)) + r"}{"
        + str(fraction.denominator) + r"}"
    )


def replace_vars_in_formula(
    tex_formula: str,
    variables: Mapping[VariableNameType, str]
) -> str:
    macros: dict[str, Callable[[str], str]] = {
        # Just variable value.
        "VAR": lambda var_name: variables[var_name],
        
        # Variable value with brackets if negative.
        "BVAR": (
            lambda var_name: (
                f"({variables[var_name]})"
                if variables[var_name].startswith("-")
                else variables[var_name]
            )
        ),

        # Variable value with "+" or "-" sign.
        "SVAR": (
            lambda var_name: (
                ("+" if not variables[var_name].startswith("-") else "")
                + variables[var_name]
            )
        ),
        
        # "-" if variable value is -1, "" if it is 1, otherwise variable value.
        "CVAR": (
            lambda var_name: (
                "-" if variables[var_name] == "-1" else (
                    "" if variables[var_name] == "1" else variables[var_name]
                )
            )
        ),
        
        # "-" if variable value is -1, "+" if it is 1, otherwise variable value with "+" or "-" sign.
        "CSVAR": (
            lambda var_name: (
                (
                    "-" if variables[var_name] == "-1" else (
                        "+" if variables[var_name] == "1" else (
                            ("+" if not variables[var_name].startswith("-") else "")
                            + variables[var_name]
                        )
                    )
                )
            )
        )
    }

    output_formula = tex_formula

    for macro_name, macro in macros.items():
        parts = output_formula.split("\\" + macro_name + "{")
        result: list[str] = [parts[0]]
        
        for part in parts[1:]:
            variable_name, rest = part[0], part[2:]
            result.extend((macro(variable_name), rest))

        output_formula = "".join(result)

    return output_formula


def two_column_images(images: Sequence[bytes], dividers: bool) -> None:
    if dividers:
        with hd.box(width="100%", margin_bottom=1):
            hd.divider()

    with hd.box(width="100%"):
        with hd.box(width="100%", horizontal_scroll=True):
            with hd.hbox(
                width="100%",
                height="100%",
                justify="space-between",
                gap=5,
            ):
                for column in range(0, 2):
                    with (
                        hd.scope(column),
                        hd.box(
                            align="start",
                            justify="start",
                        )
                    ):
                        for i, image in enumerate(images[column::2]):
                            with hd.scope(i):
                                hd.image(image, height=2, margin_top=1.25)


def solution_to_string_variables(
    solution: Mapping[VariableNameType, VariableValueType],
    proper: Mapping[VariableNameType, bool]
) -> dict[VariableNameType, str]:
    variables: dict[VariableNameType, str] = {}

    for variable_name, variable_value in solution.items():
        if variable_value == float("-inf"):
            variables[variable_name] = "NaN"
        elif proper[variable_name]:
            variables[variable_name] = float_to_tex_proper_fraction(variable_value)
        elif variable_value.is_integer():
            variables[variable_name] = str(int(variable_value))
        else:
            variables[variable_name] = str(variable_value)

    return variables


def show_solutions(
    solutions: Iterable[Mapping[VariableNameType, VariableValueType]],
    proper: Mapping[VariableNameType, bool],
    tex_formula_generator: Callable[[Mapping[VariableNameType, str]], str],
    image_generator: TexImageGenerator,
    dividers: bool = True
) -> None:
    solutions_tuple = tuple(solutions)
    images: list[bytes] = []

    for i, solution in enumerate(solutions_tuple):
        variables = solution_to_string_variables(solution, proper)

        image = image_generator(
            str(i + 1) + r") \; " + tex_formula_generator(variables)
        )

        images.append(image)

    two_column_images(images, dividers)
