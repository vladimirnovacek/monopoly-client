import tkinter as tk


class DragDropMixin(tk.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        make_draggable(self)


def make_draggable(widget: 'DragDropMixin'):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)


def on_drag_start(event: tk.Event):
    widget = event.widget
    widget.drag_start_x = event.x
    widget.drag_start_y = event.y


def on_drag_motion(event: tk.Event):
    widget = event.widget
    x = widget.winfo_x() - widget.drag_start_x + event.x
    y = widget.winfo_y() - widget.drag_start_y + event.y
    widget.place(x=x, y=y, anchor="se")
