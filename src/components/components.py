from generator.types import (
    FormulaType,
    Interval,
    Solution,
    VariableNameType,
    VariableProperties,
    GenerationTask
)
from generator import generate_solutions, evaluate
import components.coefficients_setup as cs
from components.tex_image_generator import (
    show_solutions,
    TexImageGenerator,
    replace_vars_in_formula
)

from collections import defaultdict
from typing import Annotated, Iterable, Mapping, Callable, Any

import hyperdiv as hd


@hd.global_state
class GeneratorState(hd.BaseState):
    """State that is being passed to the generator components."""

    variables: dict[VariableNameType, VariableProperties] = hd.Prop(hd.Any, dict())
    proper: dict[VariableNameType, bool] = hd.Prop(hd.Any, dict())
    conditions: set[FormulaType] = hd.Prop(hd.Any, set())
    num_of_solutions: int = hd.Prop(hd.Any, int())
    solutions: list[Solution] | None = hd.Prop(hd.Any, list())

    answer_variables: Mapping[VariableNameType, str] = hd.Prop(hd.Any, dict())
    proper_fraction_variables: Mapping[VariableNameType, bool] = hd.Prop(hd.Any, dict())
    answers: list[Solution] | None = hd.Prop(hd.Any, list())

    location: str = hd.Prop(hd.Any, str())

    def reset_component(self) -> None:
        super().reset_component()

        self.variables = defaultdict(
            lambda: VariableProperties(Interval(float(), float()), False, False)
        )
        self.proper = defaultdict(lambda: False)
        self.conditions = set()
        self.num_of_solutions = int()
        self.solutions = list()
        self.answer_variables = dict()
        self.proper_fraction_variables = dict()
        self.answers = list()

    def reset_if_location_changed(self) -> None:
        location = hd.location().path
        if self.location != location:
            self.reset_component()
        self.location = location

    def get_answers(self) -> None:
        if not self.solutions:
            self.answers = None
            return

        self.answers = list()

        for solution in self.solutions:
            variables: dict[VariableNameType, float] = {
                var_name: round(evaluate(var_formula, solution), 4)
                for var_name, var_formula in self.answer_variables.items()
            }

            self.answers.append(Solution(variables, solution))

    def get_solutions(self, loading_button: hd.button) -> None:
        conditions = self.conditions
        variables = self.variables
        num_of_equations = self.num_of_solutions
        generator_location = hd.location().path

        solutions_set = generate_solutions(
            variables,
            conditions,
            num_of_equations,
            generator_location
        )

        if solutions_set is None:
            self.solutions = None
            self.answers = None
            loading_button.loading = False
            return

        self.solutions = list(solutions_set)

        for variable_name, variable_properties in self.variables.items():
            self.proper[variable_name] = variable_properties.is_proper_fraction

        self.get_answers()
        loading_button.loading = False


def heading(tex_formula: str, image_generator: TexImageGenerator) -> None:
    """A component for displaying the heading of the generator page.
    Consists of an image of a formula.
    Also resets the generator state if the page is changed.
    """
    
    hd.image(image_generator(tex_formula, 0.02), height=2.8)


def coefficients_setup_section(
    state: GeneratorState,
    variables_defaults: Mapping[
        VariableNameType, tuple[
            Annotated[str, "default from"],
            Annotated[str, "default to"]
        ]
    ],
    fractions_avaliable: bool = True
) -> None:
    """A component for setting up coefficients.
    Consists of an interval setup and a checkbox for proper and decimal fractions
    for each variable (coefficient).
    """
    
    hd.h3("Налаштування коефіцієнтів", margin_top=1.5)
    state.reset_if_location_changed()

    for i, (
        variable_name, (default_start, default_stop)
    ) in enumerate(variables_defaults.items()):
        with hd.scope(i):
            num_range = cs.numbers_range(variable_name, default_start, default_stop)
        
        start, stop = cs.get_interval(num_range)
        state.variables[variable_name].interval.start = start
        state.variables[variable_name].interval.stop = stop

    if fractions_avaliable:
        with hd.box(margin_top=1):
            proper, decimal = cs.get_fractions(*variables_defaults.keys())
            
            for variable_name, is_proper_fraction in proper.items():
                state.variables[variable_name].is_proper_fraction = is_proper_fraction
            for variable_name, is_decimal_fraction in decimal.items():
                state.variables[variable_name].is_decimal_fraction = is_decimal_fraction


def extra_conditions_section(
    state: GeneratorState,
    extra_conditions: Iterable[
        tuple[
            Annotated[str, "description"],
            Annotated[str, "TeX formula"],
            Annotated[FormulaType, "generator conditon"]
        ]
    ] = tuple(),
    default_conditions: Iterable[FormulaType] = tuple()
) -> None:
    """A component for setting up extra conditions.
    Consists of a checkbox and an image of a formula after it for each condition.
    """

    hd.h3("Додаткові умови", margin_top=2, margin_bottom=1.25)
    state.reset_if_location_changed()

    for condition in default_conditions:
        state.conditions.add(condition)

    if extra_conditions:
        with hd.box():
            for i, (description, tex_formula, condition) in enumerate(extra_conditions):
                with hd.scope(i):
                    condition_checkbox = cs.extra_condition(description, tex_formula)
                    if condition_checkbox.checked:
                        state.conditions.add(condition)
                    else:
                        state.conditions.discard(condition)


def _solution_generation_error() -> None:
    """A component for displaying an error message when the generation fails.
    Consists of a message (as hyperdiv.text) of a red color.
    """

    hd.text(
        "Неможливо згенерувати достатньо унікальних прикладів.<br>"
        "Перевірте правильність вхідних даних.",
        font_color=hd.Color.danger,
        margin_top=2
    )


def generation_section(
    state: GeneratorState,
    tex_formula: str,
    solution_image_generator: TexImageGenerator
) -> None:
    """A component for generating and displaying solutions.
    Consists of a button for generating solutions.
    If the button is clicked, the solutions are generated and displayed.
    If the generation fails, an error message is displayed.
    """

    hd.h3("Генерація", margin_top=2)
    state.reset_if_location_changed()

    state.num_of_solutions = cs.num_of_equations()
    generate_btn = hd.button("Генерувати", margin_top=2)

    generation_task = GenerationTask()

    if generation_task.running:
        with hd.box(padding=(12, 0, 12, 0)):
            hd.text(
                "Генерація прикладів...",
                font_color=hd.Color.neutral_400,
                font_size=hd.FontSize.two_x_large
            )
        return

    if generate_btn.clicked:
        generate_btn.loading = True
        generation_task.rerun(state.get_solutions, generate_btn)

    if state.solutions:
        hd.h3("Результати генерації", margin_bottom=1.5, margin_top=2)

        show_solutions(
            state.solutions,
            state.proper,
            lambda variables: replace_vars_in_formula(tex_formula, variables),
            solution_image_generator
        )
    if state.solutions is None:
        _solution_generation_error()


def answers_section(
    state: GeneratorState,
    answer_variables: Mapping[VariableNameType, str],
    proper_fraction_variables: Mapping[VariableNameType, bool],
    tex_formula_generator: Callable[[Mapping[VariableNameType, str]], str],
    solution_image_generator: TexImageGenerator,
) -> None:
    """A component for displaying the answers.
    Shows up only if the solutions are generated.
    Consists of a button, if clicked, an image of a formula (answer)
    for each answer is displayed.
    """

    state.reset_if_location_changed()

    generation_task = GenerationTask()

    if generation_task.running:
        return

    state.answer_variables = answer_variables
    state.proper_fraction_variables = proper_fraction_variables

    if not state.answers:
        return

    with hd.details("Відповіді", width="100%", margin_top=4, margin_bottom=3):
        show_solutions(
            state.answers,
            {**proper_fraction_variables, **state.proper},
            tex_formula_generator,
            solution_image_generator,
            dividers=False
        )
