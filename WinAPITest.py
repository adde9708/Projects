import win32gui as gui
import win32con as con


def win_api():
    window_name = r'PyCharm'
    hwnd = gui.FindWindow(None, window_name)
    gui.SetForegroundWindow(hwnd)


win_api()
