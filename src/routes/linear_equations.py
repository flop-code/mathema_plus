import components as cp
from components.tex_image_generator import get_cached_image_generator

import registrar

import hyperdiv as hd


linear_equations_registrar = registrar.registrar(
    "Лінійні Рівняння",
    "linear_equations"
)

_get_image_cached = get_cached_image_generator()
_solutions_image_generator = get_cached_image_generator()


@linear_equations_registrar("Просте")
def simple():
    state = cp.GeneratorState()

    cp.heading(r"x + a = b", _get_image_cached)

    cp.coefficients_setup_section(
        state,
        {
            "a": ("5", "40"),
            "b": ("5", "40")
        }
    )
    
    cp.extra_conditions_section(
        state,
        (
            (
                "Розвʼязок є невідʼємним",
                r"x \geq 0",
                r"b >= a"
            ),
            (
                "Розвʼязок є цілим",
                r"x \in \mathbb{Z}",
                r"(b - a).is_integer()"
            )
        ),
        (r"a != 0",)
    )

    cp.generation_section(state, r"x \SVAR{a} = \VAR{b}", _solutions_image_generator)
    
    cp.answers_section(
        state,
        {"x": "b - a"},
        {"x": state.proper["a"] and state.proper["b"]},
        lambda variables:
            cp.replace_vars_in_formula(r"x = \VAR{x}", variables),
        _solutions_image_generator
    )


@linear_equations_registrar("Загальне")
def general():
    state = cp.GeneratorState()

    cp.heading(r"ax + b = c", _get_image_cached)

    cp.coefficients_setup_section(
        state,
        {
            "a": ("2", "9"),
            "b": ("5", "40"),
            "c": ("5", "40")
        }
    )
    
    cp.extra_conditions_section(
        state,
        (
            (
                "Розвʼязок є невідʼємним",
                r"x \geq 0",
                r"c >= b"
            ),
            (
                "Розвʼязок є цілим",
                r"x \in \mathbb{Z}",
                r"(c - b) % a == 0"
            ),
            (
                "Розвʼязок не є нулем",
                r"x \neq 0",
                r"b != c"
            )
        ),
        (r"a != 0 and b != 0",)
    )

    cp.generation_section(state, r"\CVAR{a}x \SVAR{b} = \VAR{c}", _solutions_image_generator)

    cp.answers_section(
        state,
        {"x": "(c - b) / a"},
        {"x": True},
        lambda variables:
            cp.replace_vars_in_formula(r"x = \VAR{x}", variables),
        _solutions_image_generator
    )
