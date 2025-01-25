from wx import (
    ALIGN_CENTER,
    EVT_LEFT_DOWN,
    HORIZONTAL,
    ICON_INFORMATION,
    ID_ANY,
    OK,
    VERTICAL,
    App,
    BoxSizer,
    Button,
    Frame,
    MessageBox,
    Panel,
)


def on_button_press(event):

    message_box = MessageBox("Button was clicked!", "Info", OK | ICON_INFORMATION)

    return message_box


def create_button(panel, sizer):

    button = Button(panel, label="Click Me")

    button.Bind(EVT_LEFT_DOWN, on_button_press)

    sizer.Add(button, 0, ALIGN_CENTER | ALIGN_CENTER, 10)  # Centered alignment

    return button


def create_frame():

    frame = Frame(None, id=ID_ANY, title="test")

    frame.SetBackgroundColour("red")
    return frame


def create_panel(frame):

    panel = Panel(frame)
    return panel


def create_sizer(orientation):

    sizer = BoxSizer(orientation)

    return sizer


def add_main_sizer_spacer(main_sizer):

    spacer = main_sizer.AddStretchSpacer()
    return spacer


def add_button_sizer_spacer(button_sizer):

    spacer = button_sizer.AddStretchSpacer()
    return spacer


def combine_sizers(main_sizer, button_sizer):
    sizer = main_sizer.Add(button_sizer, 0, ALIGN_CENTER, 10)
    return sizer


def set_panel_sizer(panel, main_sizer):

    sizer = panel.SetSizer(main_sizer)
    return sizer


def window():

    frame = create_frame()

    panel = create_panel(frame)

    # Create a vertical BoxSizer
    main_sizer = create_sizer(VERTICAL)

    # Create a horizontal BoxSizer for the button
    button_sizer = create_sizer(HORIZONTAL)

    # Add a spacer to push the button to the bottom right
    add_main_sizer_spacer(main_sizer)  # This will take up all the vertical space

    add_button_sizer_spacer(button_sizer)  # This will push the button to the right

    create_button(panel, button_sizer)  # Create the button and add to button_sizer

    combine_sizers(main_sizer, button_sizer)  # Add button_sizer to main_sizer

    set_panel_sizer(panel, main_sizer)  # Set the sizer for the panel

    frame.Show()

    return frame


def start_app():

    app = App(False)
    return app


def start():

    app = start_app()

    frame = window()

    app.MainLoop()
    return frame


def main():

    frame = start()
    return frame


main()
