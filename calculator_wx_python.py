import re
from ast import literal_eval
from functools import partial
from secrets import choice
import wx


def get_shared_state():
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


def create_solution_text(panel):
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


def handle_button_press(event, shared_state):
    button = event.GetEventObject()
    solution = button.GetParent().FindWindowByName("solution_text")
    label = button.GetLabel()
    current = solution.GetValue()
    operators = shared_state["operators"]
    redundant_operator = (
        current and current.endswith(tuple(operators)) and label in operators
    )

    if label == "C":
        solution.Clear()
        del solution
        return

    elif not redundant_operator:
        return solution.SetValue(current + label)


def show_error_message(message):
    return wx.MessageBox(message, "Error", wx.OK | wx.ICON_ERROR)


def handle_solution(event, shared_state):
    parent = event.GetEventObject().GetParent()
    solution = parent.FindWindowByName("solution_text")
    expression = solution.GetValue().strip()
    expression_pattern = shared_state["expression_pattern"]

    if not expression:
        return

    try:
        result = literal_eval(expression)
        solution.SetValue(str(result))
    except (ValueError, SyntaxError):
        if expression_pattern.fullmatch(expression):
            try:
                return solution.SetValue(str(eval(expression)))
            except Exception as e:
                return show_error_message(f"Error in expression: {e}")
        else:
            return show_error_message(
                "The entered expression is invalid. Please correct it."
            )


def bind_events(shared_state, label, button):
    if label == "=":
        return button.Bind(
            wx.EVT_LEFT_DOWN,
            partial(handle_solution, shared_state=shared_state),
        )
    button_handler = partial(handle_button_press, shared_state=shared_state)
    return button.Bind(wx.EVT_LEFT_DOWN, button_handler)


def put_button_in_panel(panel, colors, label):
    button = wx.Button(panel, label=label, size=(80, 60))
    button.SetBackgroundColour(choice(colors))
    return button


def add_button_to_hbox_sizer(hbox_sizer, button):
    hbox_sizer.Add(button, 1, flag=wx.EXPAND | wx.ALL, border=5)


def add_hbox_sizer_to_vbox(sizer, hbox_sizer):
    sizer.Add(hbox_sizer, flag=wx.EXPAND)


def create_buttons(panel, shared_state, sizer):
    colors = shared_state["colors"]
    buttons = shared_state["buttons"]

    for row in buttons:
        hbox_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for label in row:
            button = put_button_in_panel(panel, colors, label)

            # Bind events based on button label
            bind_events(shared_state, label, button)

            add_button_to_hbox_sizer(hbox_sizer, button)

        add_hbox_sizer_to_vbox(sizer, hbox_sizer)


def create_panel(frame, shared_state):
    panel = wx.Panel(frame)
    sizer = wx.BoxSizer(wx.VERTICAL)

    solution = create_solution_text(panel)
    sizer.Add(solution, flag=wx.EXPAND | wx.ALL, border=10)

    create_buttons(panel, shared_state, sizer)

    panel.SetSizer(sizer)


def create_calculator():
    shared_state = get_shared_state()

    app = wx.App()
    frame = wx.Frame(None, title="Calculator", size=(400, 500))

    create_panel(frame, shared_state)

    frame.Centre()
    frame.Show()
    app.MainLoop()


def main():
    create_calculator()


if __name__ == "__main__":
    main()
