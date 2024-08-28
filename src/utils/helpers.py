import tkinter as tk

def clear_view(widget):
    for child in widget.winfo_children():
        child.destroy()
