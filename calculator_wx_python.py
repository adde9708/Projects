import re
from ast import literal_eval
from functools import partial
from secrets import choice
from typing import Any, Dict, Tuple

import wx


def get_shared_state() -> Dict[str, Any]:
    """Encapsulates shared state and configuration."""
    return {
        "operators": {"/", "*", "+", "-"},
        "colors": (
            wx.Colour(255, 0, 0),
            wx.Colour(0, 255, 0),
            wx.Colour(0, 255, 255),
            wx.Colour(255, 255, 255),
        ),
        "expression_pattern": re.compile(r"^\d+(\.\d+)?([+\-*/]\d+(\.\d+)?)*$"),
        "buttons": (
            ("7", "8", "9", "/"),
            ("4", "5", "6", "*"),
            ("1", "2", "3", "-"),
            (".", "0", "C", "+"),
            ("=",),
        ),
    }


def create_solution_text(panel: wx.Panel) -> wx.TextCtrl:
    solution = wx.TextCtrl(
        panel,
        name="solution_text",
        style=wx.TE_RIGHT | wx.TE_READONLY,
        size=(400, 64),
    )
    solution.SetFont(
        wx.Font(
            16,
            wx.FONTFAMILY_DEFAULT,
            wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD,
        )
    )
    return solution


def handle_button_press(event: wx.CommandEvent, shared_state: Dict[str, Any]) -> None:
    button = event.GetEventObject()
    solution = button.GetParent().FindWindowByName("solution_text")
    label: str = button.GetLabel()
    current: str = solution.GetValue()
    operators = shared_state["operators"]

    if label == "C":
        solution.Clear()
        del solution
        return

    elif not ((current and current.endswith(tuple(operators)) and label in operators)):
        solution.SetValue(current + label)


def show_error_message(message: str) -> Any:
    return wx.MessageBox(message, "Error", wx.OK | wx.ICON_ERROR)


def handle_solution(event: wx.CommandEvent, shared_state: Dict[str, Any]) -> None:
    parent = event.GetEventObject().GetParent()
    solution = parent.FindWindowByName("solution_text")
    expression: str = solution.GetValue().strip()
    expression_pattern = shared_state["expression_pattern"]

    if not expression:
        return

    try:
        result = literal_eval(expression)
        solution.SetValue(str(result))
    except (ValueError, SyntaxError):
        if expression_pattern.fullmatch(expression):
            try:
                solution.SetValue(str(eval(expression)))
            except Exception as e:
                show_error_message(f"Error in expression: {e}")
        else:
            show_error_message("The entered expression is invalid. Please correct it.")


def bind_events(shared_state: Dict[str, Any], label: str, button: wx.Button) -> Any:
    if label == "=":
        return button.Bind(
            wx.EVT_LEFT_DOWN,
            partial(handle_solution, shared_state=shared_state),
        )
    button_handler = partial(handle_button_press, shared_state=shared_state)
    return button.Bind(wx.EVT_LEFT_DOWN, button_handler)


def put_button_in_panel(
    panel: wx.Panel, colors: Tuple[wx.Colour, ...], label: str
) -> wx.Button:
    button = wx.Button(panel, label=label, size=(80, 60))
    button.SetBackgroundColour(choice(colors))
    return button


def add_button_to_hbox_sizer(
    hbox_sizer: wx.BoxSizer, button: wx.Button
) -> wx.SizerItem:
    return hbox_sizer.Add(button, 1, flag=wx.EXPAND | wx.ALL, border=5)


def add_hbox_sizer_to_vbox(sizer: wx.BoxSizer, hbox_sizer: wx.BoxSizer) -> wx.SizerItem:
    return sizer.Add(hbox_sizer, flag=wx.EXPAND)


def create_buttons(
    panel: wx.Panel, shared_state: Dict[str, Any], sizer: wx.BoxSizer
) -> None:
    colors = shared_state["colors"]
    buttons = shared_state["buttons"]

    for row in buttons:
        hbox_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for label in row:
            button = put_button_in_panel(panel, colors, label)
            bind_events(shared_state, label, button)
            add_button_to_hbox_sizer(hbox_sizer, button)
        add_hbox_sizer_to_vbox(sizer, hbox_sizer)


def create_panel(frame: wx.Frame, shared_state: Dict[str, Any]) -> None:
    panel = wx.Panel(frame)
    sizer = wx.BoxSizer(wx.VERTICAL)
    solution = create_solution_text(panel)
    sizer.Add(solution, flag=wx.EXPAND | wx.ALL, border=10)
    create_buttons(panel, shared_state, sizer)
    panel.SetSizer(sizer)


def create_calculator() -> None:
    shared_state = get_shared_state()
    app = wx.App()
    frame = wx.Frame(None, title="Calculator", size=(400, 500))
    create_panel(frame, shared_state)
    frame.Centre()
    frame.Show()
    app.MainLoop()


def main() -> None:
    create_calculator()


if __name__ == "__main__":
    main()
