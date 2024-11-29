import wx
from ast import literal_eval
from secrets import choice
import re
from functools import partial


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


def handle_button_press(event, operators):

    button = event.GetEventObject()
    solution = button.GetParent().FindWindowByName("solution_text")
    label = button.GetLabel()
    current = solution.GetValue()

    if label == "C":
        solution.Clear()
    elif not (current and current[-1] in operators and label in operators):
        solution.SetValue(current + label)


def show_error_message(message):

    return wx.MessageBox(message, "Error", wx.OK | wx.ICON_ERROR)


def handle_solution(event, expression_pattern):

    solution = event.GetEventObject().GetParent().FindWindowByName("solution_text")
    expression = solution.GetValue().strip()

    if not expression:
        return

    try:
        # Safe evaluation with literal_eval
        result = literal_eval(expression)
        solution.SetValue(str(result))
        return

    except (ValueError, SyntaxError):
        # Fallback to eval for valid patterns
        if expression_pattern.fullmatch(expression):

            try:
                solution.SetValue(str(eval(expression)))
                return

            except Exception as e:
                return show_error_message(f"Error in expression: {e}")
        else:
            return show_error_message(
                "The entered expression is invalid. Please correct it."
            )


def bind_events(operators, expression_pattern, label, button):
    if label == "=":
        button.Bind(
            wx.EVT_LEFT_DOWN,
            partial(handle_solution, expression_pattern=expression_pattern),
        )

    else:
        button.Bind(wx.EVT_LEFT_DOWN, partial(handle_button_press, operators=operators))


def put_button_in_panel(panel, colors, label):
    button = wx.Button(panel, label=label, size=(80, 60))
    button.SetBackgroundColour(choice(colors))
    return button


def add_button_to_hbox_sizer(hbox_sizer, button):
    hbox_sizer = hbox_sizer.Add(button, 1, flag=wx.EXPAND | wx.ALL, border=5)
    return hbox_sizer


def add_hbox_sizer_to_vbox(sizer, hbox_sizer):
    sizer = sizer.Add(hbox_sizer, flag=wx.EXPAND)
    return sizer


def create_buttons(panel, buttons, colors, operators, expression_pattern, sizer):
    for row in buttons:
        hbox_sizer = wx.BoxSizer(wx.HORIZONTAL)
        for label in row:
            button = put_button_in_panel(panel, colors, label)

            # Bind events based on button label
            bind_events(operators, expression_pattern, label, button)

            add_button_to_hbox_sizer(hbox_sizer, button)

        add_hbox_sizer_to_vbox(sizer, hbox_sizer)


def create_panel(frame, operators, expression_pattern, buttons, colors):
    panel = wx.Panel(frame)
    sizer = wx.BoxSizer(wx.VERTICAL)

    solution = create_solution_text(panel)
    sizer.Add(solution, flag=wx.EXPAND | wx.ALL, border=10)

    create_buttons(panel, buttons, colors, operators, expression_pattern, sizer)

    panel.SetSizer(sizer)
    return panel


def create_calculator():
    operators = ("/", "*", "+", "-")

    colors = (
        wx.Colour(255, 0, 0),
        wx.Colour(0, 255, 0),
        wx.Colour(0, 255, 255),
        wx.Colour(255, 255, 255),
    )

    expression_pattern = re.compile(r"^\d+(\.\d+)?([+\-*/]\d+(\.\d+)?)*$")

    buttons = (
        ("7", "8", "9", "/"),
        ("4", "5", "6", "*"),
        ("1", "2", "3", "-"),
        (".", "0", "C", "+"),
        ("=",),
    )

    app = wx.App()
    frame = wx.Frame(None, title="Calculator", size=(400, 500))

    create_panel(frame, operators, expression_pattern, buttons, colors)

    frame.Centre()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    create_calculator()
