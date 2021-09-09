import tkinter as tk

window = tk.Tk()
window.title("code example")
window.geometry("450x200")

app = tk.Frame(window)
app.grid()

w = tk.Label(app, text="Hello, tkinter!", font=("Comic Sans", 20))
w.grid(padx=110, pady=80)

window.mainloop()
