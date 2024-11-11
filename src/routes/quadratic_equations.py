import components as cp
from components.tex_image_generator import get_cached_image_generator

from generator.types import VariableNameType
from typing import Mapping

import registrar

import hyperdiv as hd


linear_equations_registrar = registrar.registrar(
    "Квадратні Рівняння",
    "quadratic_equations"
)

_get_image_cached = get_cached_image_generator()
_solutions_image_generator = get_cached_image_generator()


def answer_tex_formula_generator(variables: Mapping[VariableNameType, str]) -> str:
    roots: set[str] = set()

    for var_name, var_value in variables.items():
        if var_name.startswith("x") and var_value != "NaN":
            roots.add((r"\approx " if "." in var_value else "") + var_value)
    
    match len(roots):
        case 0:
            return r"x \notin \mathbb{R}"
        case 1:
            return r"x = " + roots.pop()
        case _:
            return r"x = \{" + "; ".join(sorted(roots)) + r"\}"


@linear_equations_registrar("Неповне (c = 0)")
def incomplete_c():
    state = cp.GeneratorState()

    cp.heading(r"ax^2 + bx = 0", _get_image_cached)

    cp.coefficients_setup_section(
        state,
        {
            "a": ("-12", "12"),
            "b": ("-20", "20")
        },
        fractions_avaliable=False
    )
    
    cp.extra_conditions_section(
        state,
        (
            (
                "Ненульовий розвʼязок є цілим",
                r"x_2 \in \mathbb{Z}",
                r"(a != 0) and a.is_integer() and (b % a == 0)"
            ),
        ),
        (r"a != 0 and b != 0",)
    )

    cp.generation_section(state, r"\CVAR{a}x^2 \CSVAR{b}x = 0", _solutions_image_generator)
    
    cp.answers_section(
        state,
        {"x_1": "0", "x_2": r"-(b/a)"},
        {"x_1": False, "x_2": True},
        answer_tex_formula_generator,
        _solutions_image_generator
    )



@linear_equations_registrar("Неповне (b = 0)")
def incomplete_b():
    state = cp.GeneratorState()

    cp.heading(r"ax^2 + c = 0", _get_image_cached)

    cp.coefficients_setup_section(
        state,
        {
            "a": ("-12", "12"),
            "c": ("-20", "20")
        },
        fractions_avaliable=False
    )
    
    cp.extra_conditions_section(
        state,
        (
            (
                "Розвʼязки існують",
                r"x \in \mathbb{R}",
                r"(a != 0) and (c/a <= 0)"
            ),
            (
                "Розвʼязки є цілими",
                r"x \in \mathbb{Z}",
                r"(a != 0) and (c/a <= 0) and (c % a == 0) and is_square(a) and is_square(c)"
            )
        ),
        (r"a != 0 and c != 0",)
    )

    cp.generation_section(state, r"\CVAR{a}x^2 \SVAR{c} = 0", _solutions_image_generator)

    cp.answers_section(
        state,
        {"x_1": r"-((-(c/a)) ** 0.5)", "x_2": r"(-(c/a)) ** 0.5"},
        {"x_1": False, "x_2": False},
        answer_tex_formula_generator,
        _solutions_image_generator
    )


@linear_equations_registrar("Повне")
def complete():
    state = cp.GeneratorState()

    cp.heading(r"ax^2 + bx + c = 0", _get_image_cached)

    cp.coefficients_setup_section(
        state,
        {
            "a": ("-12", "12"),
            "b": ("-20", "20"),
            "c": ("-20", "20")
        },
        fractions_avaliable=False
    )
    
    cp.extra_conditions_section(
        state,
        (
            (
                "Хоча б один розвʼязок існує",
                r"x \in \mathbb{R}",
                r"(b*b - 4*a*c) >= 0"
            ),
            (
                "Розвʼязки є цілими",
                r"x \in \mathbb{Z}",
                (
                    r"(a != 0) and (2*a).is_integer() and ((b*b - 4*a*c) >= 0) and"
                    r"((-b + ((b*b - 4*a*c)) ** 0.5) % (2*a) == 0) and "
                    r"((-b - ((b*b - 4*a*c)) ** 0.5) % (2*a) == 0)"
                )
            )
        ),
        (r"a != 0 and b != 0 and c != 0",)
    )

    cp.generation_section(state, r"\CVAR{a}x^2 \CSVAR{b}x \SVAR{c} = 0", _solutions_image_generator)
    
    cp.answers_section(
        state,
        {
            "x_1": r"((-b) - ((b*b - 4*a*c) ** 0.5))/(2*a)",
            "x_2": r"((-b) + ((b*b - 4*a*c) ** 0.5))/(2*a)"
        },
        {"x_1": False, "x_2": False},
        answer_tex_formula_generator,
        _solutions_image_generator
    )


@linear_equations_registrar("Біквадратне")
def biquadratic():
    state = cp.GeneratorState()

    cp.heading(r"ax^4 + bx^2 + c = 0", _get_image_cached)

    cp.coefficients_setup_section(
        state,
        {
            "a": ("-12", "12"),
            "b": ("-20", "20"),
            "c": ("-20", "20")
        },
        fractions_avaliable=False
    )
    
    cp.extra_conditions_section(
        state,
        (
            (
                "Хоча б 2 розвʼязки існує",
                r"x \in \mathbb{R}",
                (
                    r"(a != 0) and ((b*b - 4*a*c) >= 0) and "
                    r"(((-b + ((b*b - 4*a*c)) ** 0.5) / (2*a) >= 0) or "
                    r"((-b - ((b*b - 4*a*c)) ** 0.5) / (2*a) >= 0))"
                )
            ),
            (
                "Розвʼязки є цілими",
                r"x \in \mathbb{Z}",
                (
                    r"(a != 0) and (2*a).is_integer() and (((b*b - 4*a*c) >= 0) and "
                    r"(((-b + ((b*b - 4*a*c)) ** 0.5) / (2*a) >= 0) and "
                    r"((-b - ((b*b - 4*a*c)) ** 0.5) / (2*a) >= 0))) and "
                    
                    r"(((((-b - ((b*b - 4*a*c)) ** 0.5) % (2*a)) == 0) and "
                    r"is_square((-b - ((b*b - 4*a*c)) ** 0.5) / (2*a)))) and "
                    
                    r"(((((-b + ((b*b - 4*a*c)) ** 0.5) % (2*a)) == 0) and "
                    r"is_square((-b + ((b*b - 4*a*c)) ** 0.5) / (2*a))))"
                )
            )
        ),
        (r"a != 0 and b != 0 and c != 0",)
    )

    cp.generation_section(state, r"\CVAR{a}x^4 \CSVAR{b}x^2 \SVAR{c} = 0", _solutions_image_generator)

    cp.answers_section(
        state,
        {
            "x_1": r"-(((-b + (b**2 - 4*a*c)**0.5) / (2*a))**0.5)",
            "x_2": r"(((-b + (b**2 - 4*a*c)**0.5) / (2*a))**0.5)",
            "x_3": r"-(((-b - (b**2 - 4*a*c)**0.5) / (2*a))**0.5)",
            "x_4": r"(((-b - (b**2 - 4*a*c)**0.5) / (2*a))**0.5)",
        },
        {"x_1": False, "x_2": False, "x_3": False, "x_4": False},
        answer_tex_formula_generator,
        _solutions_image_generator
    )
