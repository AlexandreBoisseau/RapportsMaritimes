# image_resizer_modal.py

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

    def create_widgets(self):
        print('Tk.Topleve modale')
        self.open_button = tk.Button(self, text="Ouvrir une image", command=self.open_image)
        self.open_button.pack(pady=10)

        self.save_button = tk.Button(self, text="Sauvegarder l'image", command=self.save_image, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.rectangle_width_label = tk.Label(self, text="Largeur du carré:")
        self.rectangle_width_label.pack()

        self.rectangle_width_entry = tk.Entry(self)
        self.rectangle_width_entry.pack()
        self.rectangle_width_entry.insert(0, "100")

        self.rectangle_height_label = tk.Label(self, text="Hauteur du carré:")
        self.rectangle_height_label.pack()

        self.rectangle_height_entry = tk.Entry(self)
        self.rectangle_height_entry.pack()
        self.rectangle_height_entry.insert(0, "100")

        self.set_rectangle_size_button = tk.Button(self, text="Définir la taille du carré", command=self.set_rectangle_size)
        self.set_rectangle_size_button.pack(pady=10)

        self.image_canvas = tk.Canvas(self, width=600, height=400)
        self.image_canvas.pack()

        self.image_canvas.bind("<B1-Motion>", self.move_rectangle)

        self.rectangle = self.image_canvas.create_rectangle(50, 50, 150, 150, outline="red")

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
        cropped_image.save(new_file_path)
        messagebox.showinfo("Sauvegarde réussie", f"L'image a été sauvegardée avec succès sous le nom {file_name}CPY{file_ext}.")

    def move_rectangle(self, event):
        width = int(self.rectangle_width_entry.get())
        height = int(self.rectangle_height_entry.get())
        self.image_canvas.coords(self.rectangle, event.x, event.y, event.x + width, event.y + height)
    
    def set_rectangle_size(self):
        try:
            width = int(self.rectangle_width_entry.get())
            height = int(self.rectangle_height_entry.get())
        except ValueError:
            messagebox.showerror("Erreur", "Veuillez entrer des dimensions valides.")
            return

        if width <= 0 or height <= 0:
            messagebox.showerror("Erreur", "Veuillez entrer des dimensions positives.")
            return

        x1, y1, x2, y2 = self.image_canvas.coords(self.rectangle)
        self.image_canvas.coords(self.rectangle, x1, y1, x1 + width, y1 + height)

    def show_image(self):
        if self.image:
            self.thumbnail = self.image.copy()
            self.thumbnail.thumbnail((600, 400), Image.ANTIALIAS)

            self.image_canvas.delete("all")
            self.photo = ImageTk.PhotoImage(self.thumbnail)
            self.image_pos = ((self.image_canvas.winfo_width() - self.thumbnail.width) // 2, (self.image_canvas.winfo_height() - self.thumbnail.height) // 2)
            self.image_canvas.create_image(self.image_pos, image=self.photo, anchor=tk.NW)
            self.rectangle = self.image_canvas.create_rectangle(50, 50, 150, 150, outline="red")

if __name__ == "__main__":
    app = ImageResizerApp()
    app.mainloop()