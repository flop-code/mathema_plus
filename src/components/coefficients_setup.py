from components.tex_image_generator import get_cached_image_generator
from generator.types import VariableNameType

from string import digits
from typing import Annotated, Sequence

import hyperdiv as hd


_get_image_cached = get_cached_image_generator()


def numbers_range(
    variable: VariableNameType,
    start_value: str = "",
    stop_value: str = ""
) -> tuple[hd.text_input, hd.text_input]:
    """A component for setting up a range of a variable.
    Consists of two text inputs for start and stop values and an image between them.
    Returns a tuple of start and stop text inputs.
    """

    with hd.hbox(gap=1, margin_top=1.5, align="center"):
        start = hd.text_input(
            placeholder="з", width=8,
            no_spin_buttons=True, size="small", value=start_value,
        )
        hd.image(
            _get_image_cached(r"\leq \hspace{0.5} " + variable + r"\hspace{0.5} \leq"),
            height=1.5
        )
        stop = hd.text_input(
            placeholder="до", width=8,
            no_spin_buttons=True, size="small", value=stop_value,
        )

    return start, stop


def get_interval(
    num_range: tuple[hd.text_input, hd.text_input]
) -> tuple[float, float]:
    """Extract numbers from (start_input, stop_input) pairs of text inputs.
    Also filter the text inputs values.
    Returns a tuple of start and stop values.
    """

    interval: list[float] = []

    for text_input in num_range:
        s_value = text_input.value.strip().replace(",", ".")

        if s_value not in ("", "-", "+"):
            if s_value[0] in "+-":
                s_value = (
                    s_value[0] + "".join(filter(
                        lambda char: char in digits + ".",
                        s_value[1:]
                    ))
                )
            
            if s_value.count(".") > 1:
                new_value = s_value.split(".", 1)
                new_value[1] = new_value[1].replace(".", "")
                s_value = ".".join(new_value)

            try:
                value = float(s_value)
                text_input.value = s_value
            except ValueError:
                text_input.reset()
                value = float(text_input.value)
        else:
            value = 0.0

        interval.append(value)

    return interval[0], interval[1]


def extra_condition(condition: str, tex_formula: str) -> hd.checkbox:
    """A component for setting up an extra condition.
    Consists of a checkbox and an image after it.
    Returns a checkbox for the condition.
    """
    
    with hd.hbox(gap=1, margin_top=0.75, align="center"):
        checkbox = hd.checkbox(condition)
        hd.image(
            _get_image_cached("(" + tex_formula + ")"),
            height=1.5
        )
    
    return checkbox


def num_of_equations(**kwargs) -> int:
    """A component for setting up the number of equations (solutions).
    Consists of a slider and two buttons for changing the value.
    Returns the number of equations.
    """
    
    slider_state = hd.state(value=0)
    
    hd.text(
        f"Кількість прикладів — {int(slider_state.value)}",
        margin_top=2
    )
    
    with hd.hbox(
        gap="4%", width="80%",
        justify="space-between", align="center",
        margin_top=1, **kwargs
    ):
        less_button = hd.button("-", font_size=hd.FontSize.large, pill=True, width=2.5)
        
        min_value, max_value = 1, 50
        num_of_equations_slider = hd.slider(
            min_value=min_value, max_value=max_value, value=6,
            width="100%", track_active_color=hd.Color.primary,
        )

        more_button = hd.button("+", font_size=hd.FontSize.large, pill=True, width=2.5)
        
    if less_button.clicked and num_of_equations_slider.value - 1 >= min_value:
        num_of_equations_slider.value -= 1
    elif more_button.clicked and num_of_equations_slider.value + 1 <= max_value:
        num_of_equations_slider.value += 1

    slider_state.value = num_of_equations_slider.value
    
    return int(slider_state.value)


def get_fractions(*variable_names: VariableNameType) -> tuple[
    Annotated[dict[VariableNameType, bool], "proper fractions"],
    Annotated[dict[VariableNameType, bool], "decimal fractions"]
]:
    """A component for setting up proper and decimal fractions.
    Consists of two checkboxes for each variable.
    Returns a tuple of proper and decimal fractions,
    represented as a dictionary {variable_name: bool}.
    """
    
    proper_checkboxes: dict[VariableNameType, hd.checkbox] = {}
    decimal_checkboxes: dict[VariableNameType, hd.checkbox] = {}

    for i, variable_name in enumerate(variable_names):
        with hd.scope(i):
            proper_checkboxes[variable_name] = extra_condition(
                f"Коефіцієнт {variable_name} є простим дробом",
                variable_name + r" = \frac{p}{q}"
            )
            decimal_checkboxes[variable_name] = extra_condition(
                f"Коефіцієнт {variable_name} є десятковим дробом",
                variable_name + r" = n.\overline{d_1 d_2}"
            )
        
        for f_checkbox_type, s_checkbox_type in (
            (decimal_checkboxes, proper_checkboxes),
            (proper_checkboxes, decimal_checkboxes)
        ):
            f_checkbox_type[variable_name].disabled = s_checkbox_type[variable_name].checked
            f_checkbox_type[variable_name].checked = (
                False if f_checkbox_type[variable_name].disabled
                else f_checkbox_type[variable_name].checked
            )

    proper: dict[VariableNameType, bool] = {
        variable_name: checkbox.checked
        for variable_name, checkbox in proper_checkboxes.items()
    }
    decimal: dict[VariableNameType, bool] = {
        variable_name: checkbox.checked
        for variable_name, checkbox in decimal_checkboxes.items()
    }

    return proper, decimal
