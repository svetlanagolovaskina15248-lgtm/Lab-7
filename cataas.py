import io
import time
import requests
import tkinter as tk
from PIL import Image, ImageTk


def load_new_image():
    global current_photo

    try:
        headers = {
            "User-Agent": "Lab7TkinterApp/1.0"
        }

        url = f"https://cataas.com/cat?t={time.time()}"
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        image_data = io.BytesIO(response.content)
        image = Image.open(image_data).convert("RGB")
        image.thumbnail((500, 350))

        current_photo = ImageTk.PhotoImage(image)
        image_label.config(image=current_photo, text="")
        status_label.config(text="")

    except Exception as e:
        status_label.config(text=f"Ошибка: {e}")
        print("Подробная ошибка:", e)


root = tk.Tk()
root.title("Генератор котиков")
root.geometry("600x500")

current_photo = None

image_label = tk.Label(root, text="Загрузка картинки...", font=("Arial", 14))
image_label.pack(pady=20)

status_label = tk.Label(root, text="", fg="red", wraplength=550)
status_label.pack(pady=10)

button = tk.Button(root, text="Следующая картинка", command=load_new_image)
button.pack(pady=20)

load_new_image()

root.mainloop()