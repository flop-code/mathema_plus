import components as cp
from components.tex_image_generator import get_cached_image_generator

import registrar

import hyperdiv as hd


basic_arithmetic_registrar = registrar.registrar(
    "Базова Арифметика",
    "basic_arithmetic"
)

_get_image_cached = get_cached_image_generator()
_solutions_image_generator = get_cached_image_generator()


@basic_arithmetic_registrar("Додавання")
def addition():
    state = cp.GeneratorState()

    cp.heading(r"a + b", _get_image_cached)

    cp.coefficients_setup_section(
        state,
        {
            "a": ("1", "10"),
            "b": ("1", "5")
        }
    )

    cp.extra_conditions_section(
        state,
        (
            (
                "Цілий результат",
                r"a + b \in \mathbb{Z}",
                r"(a + b).is_integer()"
            ),
            (
                "Без переходу через десяток",
                r"a + b < 10",
                r"a + b < 10"
            )
        )
    )

    cp.generation_section(state, r"\VAR{a} + \BVAR{b}", _solutions_image_generator)

    cp.answers_section(
        state,
        {"x": "a + b"},
        {"x": state.proper["a"] or state.proper["b"]},
        lambda variables:
            cp.replace_vars_in_formula(r"\VAR{a} + \BVAR{b} = \VAR{x}", variables),
        _solutions_image_generator
    )


@basic_arithmetic_registrar("Віднімання")
def subtraction():
    state = cp.GeneratorState()

    cp.heading(r"a - b", _get_image_cached)

    cp.coefficients_setup_section(
        state,
        {
            "a": ("1", "10"),
            "b": ("1", "5")
        }
    )

    cp.extra_conditions_section(
        state,
        (
            (
                "Невідʼємний результат",
                r"a - b \geq 0",
                r"a - b >= 0"
            ),
        )
    )

    cp.generation_section(state, r"\VAR{a} - \BVAR{b}", _solutions_image_generator)
    
    cp.answers_section(
        state,
        {"x": "a - b"},
        {"x": state.proper["a"] or state.proper["b"]},
        lambda variables:
            cp.replace_vars_in_formula(r"\VAR{a} - \BVAR{b} = \VAR{x}", variables),
        _solutions_image_generator
    )


@basic_arithmetic_registrar("Множення")
def multiplication():
    state = cp.GeneratorState()

    cp.heading(r"a \cdot b", _get_image_cached)

    cp.coefficients_setup_section(
        state,
        {
            "a": ("2", "9"),
            "b": ("2", "9")
        }
    )

    cp.generation_section(state, r"\VAR{a} \cdot \BVAR{b}", _solutions_image_generator)
    
    cp.answers_section(
        state,
        {"x": "a * b"},
        {"x": state.proper["a"] or state.proper["b"]},
        lambda variables:
            cp.replace_vars_in_formula(r"\VAR{a} \cdot \BVAR{b} = \VAR{x}", variables),
        _solutions_image_generator
    )


@basic_arithmetic_registrar("Ділення")
def division():
    state = cp.GeneratorState()

    cp.heading(r"a : b", _get_image_cached)

    cp.coefficients_setup_section(
        state,
        {
            "a": ("10", "100"),
            "b": ("2", "9")
        }
    )

    cp.extra_conditions_section(
        state,
        (
            (
                "Цілий результат",
                r"a : b \in \mathbb{Z}",
                r"a % b == 0"
            ),
        ),
        (r"b != 0",)
    )
    
    cp.generation_section(state, r"\VAR{a} : \BVAR{b}", _solutions_image_generator)

    cp.answers_section(
        state,
        {"x": "a / b"},
        {"x": True},
        lambda variables:
            cp.replace_vars_in_formula(r"\VAR{a} : \BVAR{b} = \VAR{x}", variables),
        _solutions_image_generator
    )
