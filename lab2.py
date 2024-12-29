import os
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
import pandas as pd

def get_image_info(file_path):
    try:
        with Image.open(file_path) as img:
            return {
                "Имя файла": os.path.basename(file_path),
                "Размер (пиксели)": f"{img.width} x {img.height}",
                "Разрешение (dpi)": img.info.get('dpi', (72, 72)),
                "Глубина цвета": img.mode,
                "Сжатие": img.info.get('compression', 'N/A')
            }
    except Exception as e:
        print(f"Ошибка обработки файла {file_path}: {e}")
        return None

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        process_images(folder_path)

def process_images(folder_path):
    image_info_list = []
    valid_extensions = ('.jpg', '.jpeg', '.gif', '.tif', '.bmp', '.png', '.pcx')

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(valid_extensions):
            file_path = os.path.join(folder_path, filename)
            info = get_image_info(file_path)
            if info:
                image_info_list.append(info)

    if image_info_list:
        show_results(image_info_list)
    else:
        messagebox.showinfo("Результат", "Не найдено изображений в выбранной папке.")

def show_results(image_info_list):
    df = pd.DataFrame(image_info_list)
    result_window = Toplevel(root)
    result_window.title("Информация об изображениях")
    
    text = Text(result_window)
    text.pack(expand=True, fill=BOTH)

    text.insert(END, df.to_string(index=False))

root = Tk()
root.title("Приложение для считывания информации об изображениях")
root.geometry("400x200")

btn_select_folder = Button(root, text="Выбрать папку с изображениями", command=select_folder)
btn_select_folder.pack(pady=20)

root.mainloop()
