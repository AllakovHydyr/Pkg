import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
import os

# Функция для загрузки изображения
def load_image():
    global img, img_display, img_path
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
    if file_path:
        img_path = file_path
        img = Image.open(file_path).convert("RGB")
        display_image(img)

# Функция для отображения изображения
def display_image(image):
    global img_display
    img_resized = image.resize((400, 300))
    img_display = ImageTk.PhotoImage(img_resized)
    canvas.create_image(0, 0, anchor=tk.NW, image=img_display)

# Функция для поэлементного линейного контрастирования
def linear_contrast():
    global img
    if img is None:
        return
    img_np = np.array(img)
    img_min, img_max = img_np.min(), img_np.max()
    img_contrast = ((img_np - img_min) / (img_max - img_min) * 255).astype(np.uint8)
    img = Image.fromarray(img_contrast)
    display_image(img)

# Функция для построения и эквализации гистограммы
def histogram_equalization():
    global img
    if img is None:
        return
    img_np = np.array(img.convert("L"))  # Переводим в градации серого
    hist, bins = np.histogram(img_np.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * hist.max() / cdf.max()
    
    # Эквализация
    cdf_m = np.ma.masked_equal(cdf, 0)
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')
    img_eq = cdf[img_np]
    img = Image.fromarray(img_eq)

    # Построение гистограммы
    plt.figure(figsize=(10, 4))
    plt.subplot(1, 2, 1)
    plt.hist(img_np.flatten(), 256, [0, 256], color='blue')
    plt.title("Original Histogram")
    plt.subplot(1, 2, 2)
    plt.hist(img_eq.flatten(), 256, [0, 256], color='green')
    plt.title("Equalized Histogram")
    plt.show()

    display_image(img)

# Создание основного окна приложения
root = tk.Tk()
root.title("Image Processing Application")

# Полотно для отображения изображения
canvas = tk.Canvas(root, width=400, height=300, bg="gray")
canvas.grid(row=0, column=0, columnspan=2)

# Кнопка для загрузки изображения
btn_load = ttk.Button(root, text="Load Image", command=load_image)
btn_load.grid(row=1, column=0, padx=5, pady=5)

# Кнопка для линейного контрастирования
btn_contrast = ttk.Button(root, text="Linear Contrast", command=linear_contrast)
btn_contrast.grid(row=1, column=1, padx=5, pady=5)

# Кнопка для эквализации гистограммы
btn_histogram = ttk.Button(root, text="Equalize Histogram", command=histogram_equalization)
btn_histogram.grid(row=2, column=0, padx=5, pady=5)

# База тестовых изображений (зашумленные, размытые, малоконтрастные) 
def load_test_image(test_type):
    global img
    test_images = {
        "noisy": "test_images/noisy_image.jpg",
        "blurry": "test_images/blurry_image.jpg",
        "low_contrast": "test_images/low_contrast_image.jpg"
    }
    file_path = test_images.get(test_type)
    if file_path and os.path.exists(file_path):
        img = Image.open(file_path).convert("RGB")
        display_image(img)

# Кнопка для загрузки зашумленного изображения
btn_load_noisy = ttk.Button(root, text="Load Noisy Image", command=lambda: load_test_image("noisy"))
btn_load_noisy.grid(row=2, column=1, padx=5, pady=5)

# Запуск приложения
img = None
img_display = None
img_path = None
root.mainloop()