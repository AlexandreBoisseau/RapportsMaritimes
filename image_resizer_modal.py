import sys
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk

class ImageResizerModal(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Image Resizer")
        self.geometry("800x600")

        self.create_widgets()
        self.saved_image_path = None
        self.resizing = False
        self.resize_direction = None

    def create_widgets(self):
        self.open_button = tk.Button(self, text="Ouvrir une image", command=self.open_image)
        self.open_button.pack(pady=10)

        self.save_button = tk.Button(self, text="Sauvegarder l'image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.image_canvas = tk.Canvas(self, width=600, height=400)
        self.image_canvas.pack()

        self.image_canvas.bind("<B1-Motion>", self.move_or_resize_rectangle)
        self.image_canvas.bind("<Button-1>", self.start_move_or_resize)
        self.image_canvas.bind("<ButtonRelease-1>", self.stop_move_or_resize)
        self.image_canvas.bind("<Motion>", self.change_cursor)

        # Définissez la largeur et la hauteur en fonction du ratio 3:2
        width = 150
        height = width * 2 / 3
        self.rectangle = self.image_canvas.create_rectangle(50, 50, 50+width, 50+height, outline="red")

    def open_image(self):
        if sys.platform == "darwin":
            filetypes = [("Image files", "public.image")]
        else:
            filetypes = [("Image files", "*.jpg;*.png;*.jpeg;*.gif;*.bmp")]

        file_path = filedialog.askopenfilename(filetypes=filetypes)

        if file_path:
            self.image = Image.open(file_path)
            self.original_file_path = file_path
            self.show_image()
            self.save_button.config(state=tk.NORMAL)

    def save_image(self):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        file_name, file_ext = os.path.splitext(os.path.basename(self.original_file_path))
        new_file_path = os.path.join(file_dir, f"{file_name}CPY{file_ext}")

        x1, y1, x2, y2 = self.image_canvas.coords(self.rectangle)
        x_ratio = self.image.width / self.thumbnail.width
        y_ratio = self.image.height / self.thumbnail.height
        cropped_image = self.image.crop(((x1 - self.image_pos[0]) * x_ratio, (y1 - self.image_pos[1]) * y_ratio, (x2 - self.image_pos[0]) * x_ratio, (y2 - self.image_pos[1]) * y_ratio))

        # Redimensionnez l'image à 300x200px
        resized_image = cropped_image.resize((300, 200), Image.ANTIALIAS)

        resized_image.save(new_file_path)
        # messagebox.showinfo("Sauvegarde réussie", f"L'image a été sauvegardée avec succès sous le nom {file_name}CPY{file_ext}.")
        self.saved_image_path = new_file_path
        self.destroy()

    def get_saved_image_path(self):
        return self.saved_image_path

    def start_move_or_resize(self, event):
        self.start_x = event.x
        self.start_y = event.y
        x1, y1, x2, y2 = self.image_canvas.coords(self.rectangle)
        if abs(event.x - x2) <= 10 and abs(event.y - y2) <= 10:
            self.resizing = True
            self.resize_direction = "SE"
        elif abs(event.x - x1) <= 10 and abs(event.y - y1) <= 10:
            self.resizing = True
            self.resize_direction = "NW"
        elif abs(event.x - x2) <= 10 and abs(event.y - y1) <= 10:
            self.resizing = True
            self.resize_direction = "NE"
        elif abs(event.x - x1) <= 10 and abs(event.y - y2) <= 10:
            self.resizing = True
            self.resize_direction = "SW"

    def stop_move_or_resize(self, event):
        self.resizing = False
        self.resize_direction = None

    def move_or_resize_rectangle(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        x1, y1, x2, y2 = self.image_canvas.coords(self.rectangle)
        width, height = x2 - x1, y2 - y1
        ratio = width / height

        if self.resizing:
            if self.resize_direction == "SE":
                x2 += dx
                y2 = y1 + (x2 - x1) / ratio
            elif self.resize_direction == "NW":
                x1 += dx
                y1 = y2 - (x2 - x1) / ratio
            elif self.resize_direction == "NE":
                x2 += dx
                y1 = y2 - (x2 - x1) / ratio
            elif self.resize_direction == "SW":
                x1 += dx
                y2 = y1 + (x2 - x1) / ratio
            self.image_canvas.coords(self.rectangle, x1, y1, x2, y2)
        elif not self.resizing:
            self.image_canvas.move(self.rectangle, dx, dy)
        self.start_x = event.x
        self.start_y = event.y

    def change_cursor(self, event):
        x1, y1, x2, y2 = self.image_canvas.coords(self.rectangle)
        if abs(event.x - x2) <= 10 and abs(event.y - y2) <= 10 or abs(event.x - x1) <= 10 and abs(event.y - y1) <= 10 or abs(event.x - x2) <= 10 and abs(event.y - y1) <= 10 or abs(event.x - x1) <= 10 and abs(event.y - y2) <= 10:
            self.config(cursor="sizing")
        else:
            self.config(cursor="")

    def show_image(self):
        self.thumbnail = self.image.copy()
        self.thumbnail.thumbnail((600, 400))

        self.image_pos = ((600 - self.thumbnail.width) // 2, (400 - self.thumbnail.height) // 2)
        self.photo = ImageTk.PhotoImage(self.thumbnail)

        self.image_canvas.create_image(self.image_pos[0], self.image_pos[1], anchor=tk.NW, image=self.photo)

        # Place le rectangle au premier plan
        self.image_canvas.tag_raise(self.rectangle)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    resizer = ImageResizerModal(root)
    resizer.wait_window()

    if resizer.get_saved_image_path() is not None:
        print(f"Image sauvegardée : {resizer.get_saved_image_path()}")

    sys.exit(0)
