import tkinter as tk
from tkinter import colorchooser, messagebox
import math

# RGB ↔ XYZ
def rgb_to_xyz(r, g, b):
    r, g, b = [x / 255.0 for x in (r, g, b)]
    r = pow((r + 0.055) / 1.055, 2.4) if r > 0.04045 else r / 12.92
    g = pow((g + 0.055) / 1.055, 2.4) if g > 0.04045 else g / 12.92
    b = pow((b + 0.055) / 1.055, 2.4) if b > 0.04045 else b / 12.92

    x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
    y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
    z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041

    return (x * 100, y * 100, z * 100)

def xyz_to_rgb(x, y, z):
    x /= 100
    y /= 100
    z /= 100

    r = x * 3.2404542 + y * -1.5371385 + z * -0.4985314
    g = x * -0.9692660 + y * 1.8760108 + z * 0.0415560
    b = x * 0.0556434 + y * -0.2040259 + z * 1.0572252

    r = 1.055 * pow(r, 1 / 2.4) - 0.055 if r > 0.0031308 else r * 12.92
    g = 1.055 * pow(g, 1 / 2.4) - 0.055 if g > 0.0031308 else g * 12.92
    b = 1.055 * pow(b, 1 / 2.4) - 0.055 if b > 0.0031308 else b * 12.92

    r, g, b = [max(0, min(255, int(c * 255))) for c in (r, g, b)]
    return r, g, b

# XYZ ↔ LAB
def xyz_to_lab(x, y, z):
    ref_x, ref_y, ref_z = 95.047, 100.000, 108.883  # D65 reference white
    x, y, z = x / ref_x, y / ref_y, z / ref_z

    def f(t):
        return pow(t, 1 / 3.0) if t > 0.008856 else (7.787 * t) + (16 / 116)

    l = (116 * f(y)) - 16
    a = 500 * (f(x) - f(y))
    b = 200 * (f(y) - f(z))

    return (l, a, b)

def lab_to_xyz(l, a, b):
    ref_x, ref_y, ref_z = 95.047, 100.000, 108.883  # D65 reference white

    y = (l + 16) / 116
    x = a / 500 + y
    z = y - b / 200

    def f_inv(t):
        return pow(t, 3) if t ** 3 > 0.008856 else (t - 16 / 116) / 7.787

    x, y, z = f_inv(x), f_inv(y), f_inv(z)

    x, y, z = x * ref_x, y * ref_y, z * ref_z
    return x, y, z

# RGB ↔ CMYK
def rgb_to_cmyk(r, g, b):
    if (r == 0) and (g == 0) and (b == 0):
        return (0, 0, 0, 1)
    c = 1 - (r / 255)
    m = 1 - (g / 255)
    y = 1 - (b / 255)
    k = min(c, m, y)
    c = (c - k) / (1 - k) if k < 1 else 0
    m = (m - k) / (1 - k) if k < 1 else 0
    y = (y - k) / (1 - k) if k < 1 else 0
    return (c, m, y, k)

def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c) * (1 - k)
    g = 255 * (1 - m) * (1 - k)
    b = 255 * (1 - y) * (1 - k)
    return int(r), int(g), int(b)

# GUI Setup
root = tk.Tk()
root.title("Color Converter")
root.geometry("600x900")

# Callback to update the color display
def update_color_display(r, g, b):
    # Ensure RGB values are within valid range
    r, g, b = [max(0, min(255, int(c))) for c in (r, g, b)]
    # Update the display color
    color_display.config(bg=f'#{r:02x}{g:02x}{b:02x}')

# Update all colors based on RGB
def update_from_rgb():
    r = r_scale.get()
    g = g_scale.get()
    b = b_scale.get()

    # RGB → XYZ → LAB
    x, y, z = rgb_to_xyz(r, g, b)
    l, a, b_lab = xyz_to_lab(x, y, z)

    # RGB → CMYK
    c, m, y_cmyk, k = rgb_to_cmyk(r, g, b)

    # Update LAB sliders
    l_scale.set(l)
    a_scale.set(a)
    b_lab_scale.set(b_lab)

    # Update CMYK sliders
    c_scale.set(c * 100)
    m_scale.set(m * 100)
    y_cmyk_scale.set(y_cmyk * 100)
    k_scale.set(k * 100)

    # Update color display
    update_color_display(r, g, b)

# Update RGB from LAB
def update_from_lab():
    l = l_scale.get()
    a = a_scale.get()
    b_lab = b_lab_scale.get()

    # LAB → XYZ → RGB
    x, y, z = lab_to_xyz(l, a, b_lab)
    r, g, b = xyz_to_rgb(x, y, z)

    # Update RGB sliders
    r_scale.set(r)
    g_scale.set(g)
    b_scale.set(b)

    update_from_rgb()

# Update RGB from CMYK
def update_from_cmyk():
    c = c_scale.get() / 100.0
    m = m_scale.get() / 100.0
    y_cmyk = y_cmyk_scale.get() / 100.0
    k = k_scale.get() / 100.0

    # CMYK → RGB
    r, g, b = cmyk_to_rgb(c, m, y_cmyk, k)

    # Update RGB sliders
    r_scale.set(r)
    g_scale.set(g)
    b_scale.set(b)

    update_from_rgb()

# GUI Elements
r_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, label="R", command=lambda x: update_from_rgb())
r_scale.grid(row=0, column=0, padx=10, pady=5)
g_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, label="G", command=lambda x: update_from_rgb())
g_scale.grid(row=1, column=0, padx=10, pady=5)
b_scale = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, label="B", command=lambda x: update_from_rgb())
b_scale.grid(row=2, column=0, padx=10, pady=5)

l_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="L", command=lambda x: update_from_lab())
l_scale.grid(row=3, column=0, padx=10, pady=5)
a_scale = tk.Scale(root, from_=-128, to=128, orient=tk.HORIZONTAL, label="A", command=lambda x: update_from_lab())
a_scale.grid(row=4, column=0, padx=10, pady=5)
b_lab_scale = tk.Scale(root, from_=-128, to=128, orient=tk.HORIZONTAL, label="B", command=lambda x: update_from_lab())
b_lab_scale.grid(row=5, column=0, padx=10, pady=5)

c_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="C", command=lambda x: update_from_cmyk())
c_scale.grid(row=6, column=0, padx=10, pady=5)
m_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="M", command=lambda x: update_from_cmyk())
m_scale.grid(row=7, column=0, padx=10, pady=5)
y_cmyk_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="Y", command=lambda x: update_from_cmyk())
y_cmyk_scale.grid(row=8, column=0, padx=10, pady=5)
k_scale = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, label="K", command=lambda x: update_from_cmyk())
k_scale.grid(row=9, column=0, padx=10, pady=5)

color_display = tk.Label(root, text="", bg="white", width=40, height=10)
color_display.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
