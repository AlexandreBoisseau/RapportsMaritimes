# main_app.py

import tkinter as tk
from image_resizer_modal import ImageResizerModal
from rapport import *

class YourMainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Main app")
        self.geometry("800x600")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        self.show_image_resizer_button = tk.Button(self, text="Ouvrir le redimensionneur d'image", command=self.show_modal)
        self.show_image_resizer_button.pack(pady=10)

    def show_modal(self):
        image_resizer_modal = ImageResizerModal(self)
        image_resizer_modal.grab_set()

if __name__ == "__main__":
    app = YourMainApp()
    app.mainloop()
