import tkinter as tk


class DragDropMixin(tk.Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.drag_start_x: int = 0
        self.drag_start_y: int = 0
        make_draggable(self)


def make_draggable(widget: DragDropMixin):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)


def on_drag_start(event: tk.Event):
    widget: DragDropMixin = event.widget
    widget.drag_start_x = event.x
    widget.drag_start_y = event.y


def on_drag_motion(event: tk.Event):
    widget: DragDropMixin = event.widget
    x = widget.winfo_x() + event.x - widget.drag_start_x
    y = widget.winfo_y() + event.y - widget.drag_start_y
    widget.place(x=x, y=y, relx=0, rely=0, anchor='nw')
