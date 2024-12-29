import time
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter.messagebox import showerror
from tkinter import simpledialog

import algorithms

DEFAULT_FONT = ("Georgia", 8)


class MyApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#646e66", foreground="white")

        self.root.geometry('1000x600')
        self.root.title('Rasterization algorithms')
        self.root.minsize(700, 600)

        self.frame = ttk.Frame(self.root, height=600, width=800)
        self.frame.pack(expand=True, fill="both", side="top")

        self.root.title("Rasterization algorithms")

        self.menu_bar = ttk.Frame(self.frame)
        self.menu_bar.pack(side="left", padx=12, pady=12)

        x1_label = ttk.Label(self.menu_bar, text="x1 (x0)", background="#646e66")
        x1_label.pack(side="top")

        x1_input = ttk.Entry(self.menu_bar, validate="all", validatecommand=(self.menu_bar.register(self.check_number), "%P"))
        x1_input.pack(fill="x", pady=2, side="top")

        y1_label = ttk.Label(self.menu_bar, text="y1 (y0)", background="#646e66")
        y1_label.pack(side="top")

        y1_input = ttk.Entry(self.menu_bar, validate="all", validatecommand=(self.menu_bar.register(self.check_number), "%P"))
        y1_input.pack(fill="x", pady=2, side="top")

        x2_label = ttk.Label(self.menu_bar, text="x2 (R)", background="#646e66")
        x2_label.pack(side="top")

        x2_input = ttk.Entry(self.menu_bar, validate="all", validatecommand=(self.menu_bar.register(self.check_number), "%P"))
        x2_input.pack(fill="x", pady=2, side="top")

        y2_label = ttk.Label(self.menu_bar, text="y2", background="#646e66")
        y2_label.pack(side="top")

        y2_input = ttk.Entry(self.menu_bar, validate="all", validatecommand=(self.menu_bar.register(self.check_number), "%P"))
        y2_input.pack(fill="x", pady=2, side="top")

        separator1 = ttk.Separator(self.menu_bar, orient="horizontal")
        separator1.pack(pady=5, side="top")

        button_step = Button(self.menu_bar, text="Пошаговый алгоритм", command=self.build_step, background="#48544b")
        button_step.pack(fill="x", pady=2, side="top")

        button_dda = Button(self.menu_bar, text="Алгоритм DDA", command=self.build_dda, background="#48544b")
        button_dda.pack(fill="x", pady=2, side="top")

        button_bres = Button(self.menu_bar, text="Алгоритм Брезенхема", command=self.build_bres, background="#48544b")
        button_bres.pack(fill="x", pady=2, side="top")

        button_bres_circle = Button(self.menu_bar, text="Алгоритм Брезенхема(окружность)", command=self.build_circle, background="#48544b")
        button_bres_circle.pack(fill="x", pady=2, side="top")

        button_castle_pitway = Button(self.menu_bar, text="Алгоритм Кастла-Питвея", command=self.build_castle_pitway, background="#48544b")
        button_castle_pitway.pack(fill="x", pady=2, side="top")

        button_vu = Button(self.menu_bar, text="Алгоритм Ву", command=self.ask_m,
                                      background="#48544b")
        button_vu.pack(fill="x", pady=2, side="top")

        separator2 = ttk.Separator(self.menu_bar, orient="horizontal")
        separator2.pack(pady=5, side="top")

        scale_label = ttk.Label(self.menu_bar, text="Scale", background="#646e66")
        scale_label.pack(side="top")

        self.scale_input = ttk.Spinbox(self.menu_bar, from_=2, to=2000, command=self.update_all)
        self.scale_input.pack(side="top")

        time_label = ttk.Label(self.menu_bar, text="Time:", background="#646e66")
        time_label.pack(side="top")

        self.time_window = ttk.Entry(self.menu_bar)
        self.time_window.pack(side="top")

        self.main_frame = ttk.Frame(self.frame)
        self.main_frame.pack(expand=True, fill="both", side="right", padx=12, pady=12)

        self.canvas = tk.Canvas(self.main_frame, background="#FFFFFF")
        self.canvas.pack(expand=True, fill="both", side="top")

        self.scale = 12
        self.scale_input.set(self.scale)
        self.x1_input = x1_input
        self.y1_input = y1_input
        self.x2_input = x2_input
        self.y2_input = y2_input
        self.dots = []
        self.time = 0.0
        self.flag = False
        self.m = 0

    def run(self):
        self.root.mainloop()

    def check_number(self, value):
        return value.isdigit() or (value and value[0] == '-' and value[1:].isdigit())

    def show_alert(self):
        showerror("Error", "Wrong data")

    def update_scale(self, event=None):
        self.scale = int(self.scale_input.get())
        self.canvas.delete("all")  # Clear canvas
        self.draw_axes()
        self.draw_grid()

    def draw_axes(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.canvas.create_line(0, height / 2, width - 10, height / 2, arrow=tk.LAST)
        self.canvas.create_line(width / 2, height, width / 2, 10, arrow=tk.LAST)

    def draw_grid(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        x_spacing = width / (2 * self.scale)
        y_spacing = x_spacing

        for i in range(-self.scale, self.scale + 1):
            if i == 0:
                continue
            x = width / 2 + i * x_spacing
            self.canvas.create_line(x, 0, x, height, dash=(2, 2), fill="lightgray")

            if i != self.scale and i != -self.scale:

                if 25 <= self.scale < 50:
                    if i % 2 == 0:
                        self.canvas.create_text(x, height / 2 + 4, text=str(i), anchor=tk.N, font=DEFAULT_FONT)
                elif self.scale >= 50:
                    if i % 5 == 0:
                        self.canvas.create_text(x, height / 2 + 4, text=str(i), anchor=tk.N, font=DEFAULT_FONT)
                else:
                    self.canvas.create_text(x, height / 2 + 4, text=str(i), anchor=tk.N, font=DEFAULT_FONT)

        y_scale = int(height / (2 * y_spacing))
        for i in range(-y_scale, y_scale + 1):
            if i == 0:
                continue
            y = height / 2 + i * y_spacing
            self.canvas.create_line(0, y, width, y, dash=(2, 2), fill="lightgray")

            if i != y_scale and i != -y_scale:

                if 25 <= self.scale < 50:
                    if i % 2 == 0:
                        self.canvas.create_text(width / 2 + 4, y, text=str(-i), anchor=tk.NW, font=DEFAULT_FONT)
                elif self.scale >= 50:
                    if i % 5 == 0:
                        self.canvas.create_text(width / 2 + 4, y, text=str(-i), anchor=tk.NW, font=DEFAULT_FONT)
                else:
                    self.canvas.create_text(width / 2 + 4, y, text=str(-i), anchor=tk.NW, font=DEFAULT_FONT)

        # draw zero
        self.canvas.create_text(width / 2 + 4, height / 2 + 4, text="0", anchor=tk.NW, font=DEFAULT_FONT)

    def draw_dot(self, x, y):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        x_spacing = width / (2 * self.scale)
        y_spacing = x_spacing

        x_0 = x
        y_0 = y

        x = width / 2 + x * x_spacing
        y = height / 2 - y * y_spacing

        if self.flag:
            color_min = 0
            color_max = 255
            colors = []
            delta = int((color_max - color_min) / (self.m - 1))
            for i in range(self.m):
                temp = color_min + delta * i
                hex_value = '#{:02x}{:02x}{:02x}'.format(temp, temp, temp)
                colors.append(hex_value)
            self.canvas.create_rectangle(x, y, x + x_spacing, y - y_spacing, fill=colors[self.dots[(x_0,y_0)]])
        else:
            color = "#48544b"
            self.canvas.create_rectangle(x, y, x + x_spacing, y - y_spacing, fill=color)

    def update_dots(self):
        for dot in self.dots:
            self.draw_dot(dot[0], dot[1])

    def update_all(self, event=None):
        self.canvas.delete("all")
        self.time_window.delete(0, "end")
        self.time_window.insert(0, str(self.time))
        self.update_scale(event)
        self.draw_grid()
        self.draw_axes()
        self.update_dots()

    def get_dots(self, circle=False):
        try:
            arr = []
            for input_el in (self.x1_input, self.y1_input, self.x2_input, self.y2_input):
                arr.append(float(input_el.get().replace(',', '.')))
            if arr[0] == arr[2] and arr[1] == arr[3] and not circle:
                self.show_alert()
                return None
            return tuple(arr)
        except:
            self.show_alert()
            return None

    def build_step(self):
        self.flag = False
        self.dots = []
        start_dots = self.get_dots()
        if start_dots is None:
            return

        start_time = time.time()
        self.dots = algorithms.step_by_step(*start_dots)
        end_time = time.time()
        self.time = end_time - start_time
        self.update_all()

    def build_dda(self):
        self.flag = False
        self.dots = []
        start_dots = self.get_dots()
        if start_dots is None:
            return

        start_time = time.time()
        self.dots = algorithms.dda(*start_dots)
        end_time = time.time()
        self.time = end_time - start_time
        self.update_all()

    def build_bres(self):
        self.flag = False
        self.dots = []
        start_dots = self.get_dots()
        if start_dots is None:
            return

        start_time = time.time()
        self.dots = algorithms.bresenhem(*start_dots)
        end_time = time.time()
        self.time = end_time - start_time
        self.update_all()

    def build_circle(self):
        self.flag = False
        self.dots = []
        start_dots = self.get_dots()
        if start_dots is None:
            return

        start_time = time.time()
        self.dots = algorithms.bresenham_circle(*start_dots[:3])
        end_time = time.time()
        self.time = end_time - start_time
        self.update_all()

    def build_castle_pitway(self):
        self.flag = False
        self.dots = []
        start_dots = self.get_dots()
        if start_dots is None:
            return

        start_time = time.time()
        self.dots = algorithms.kastla_pitveya(*start_dots)
        end_time = time.time()
        self.time = end_time - start_time
        self.update_all()

    def build_vu(self):
        self.dots = []
        self.flag = True
        start_dots = self.get_dots()
        if start_dots is None:
            return

        start_time = time.time()
        self.dots = algorithms.wu(*start_dots, self.m)
        end_time = time.time()
        self.time = end_time - start_time
        self.update_all()

    def ask_m(self):
        m = simpledialog.askinteger('', 'Enter the number of shades:')
        if m is not None:
            self.m = m
            self.build_vu()
        else:
            showerror('Wrong data! Try again')


if __name__ == "__main__":
    app = MyApp()
    app.run()
