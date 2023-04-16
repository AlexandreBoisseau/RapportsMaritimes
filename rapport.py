import tkinter as tk
import subprocess
import shutil
import fileinput
from PIL import ImageTk, Image
from tkinter import PhotoImage
from image_resizer_modal import ImageResizerModal

template_file = 'template_file.tex'
output_file = 'rapport.tex'

liste_des_pages = []
liste_des_canvas = []
liste_des_images = []

actual_page_number = 0


class YourMainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # =================================================== #
        # Création de la fenêtre principale
        self.title("Exemple avec label, champ de texte et bouton")
        # =================================================== #


        # =================================================== #
        # Création et placement du label
        label = tk.Label(self, text="Titre du rapport :")
        label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Création et placement du champ de texte
        global champ_texte
        champ_texte = tk.Entry(self)
        champ_texte.grid(row=1, column=0, padx=10, pady=10)

        # Création et placement du bouton
        global buton
        bouton = tk.Button(self, text="Afficher")
        bouton["command"] = lambda: afficher_texte(champ_texte)
        bouton.grid(row=1, column=1, padx=10, pady=10)

        global liste_des_canvas
        liste_des_canvas.append((label, label.grid_info()))
        liste_des_canvas.append((champ_texte, champ_texte.grid_info()))
        liste_des_canvas.append((bouton, bouton.grid_info()))
        # =================================================== #

        # =================================================== #
        # TEMPLATE TITRE + CHAMP + BOUTTON A REPETER A LENVIE #
        global label2
        label2 = tk.Label(self, text="Date de l'expertise :")
        label2.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        global champ_texte2
        champ_texte2 = tk.Entry(self)
        champ_texte2.grid(row=3, column=0, padx=10, pady=10)

        global bouton2
        bouton2 = tk.Button(self, text="Afficher")
        bouton2["command"] = lambda: afficher_texte(champ_texte2)
        bouton2.grid(row=3, column=1, padx=10, pady=10)

        liste_des_canvas.append((label2, label2.grid_info()))
        liste_des_canvas.append((champ_texte2, champ_texte2.grid_info()))
        liste_des_canvas.append((bouton2, bouton2.grid_info()))
        # =================================================== #

        # =================================================== #
        # TEMPLATE TITRE + CHAMP + BOUTTON A REPETER A LENVIE #
        global label3
        label3 = tk.Label(self, text="Nom du cabinet :")
        label3.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        global champ_texte3
        champ_texte3 = tk.Entry(self)
        champ_texte3.grid(row=5, column=0, padx=10, pady=10)

        global bouton3
        bouton3 = tk.Button(self, text="Afficher")
        bouton3["command"] = lambda: afficher_texte(champ_texte3)
        bouton3.grid(row=5, column=1, padx=10, pady=10)

        liste_des_canvas.append((label3, label3.grid_info()))
        liste_des_canvas.append((champ_texte3, champ_texte3.grid_info()))
        liste_des_canvas.append((bouton3, bouton3.grid_info()))
        # =================================================== #

        # =================================================== #
        # TEMPLATE TITRE + CHAMP + BOUTTON A REPETER A LENVIE #
        global label4
        label4 = tk.Label(self, text="Nom du navire :")
        label4.grid(row=6, column=0, padx=10, pady=10, sticky="w")

        global champ_texte4
        champ_texte4 = tk.Entry(self)
        champ_texte4.grid(row=7, column=0, padx=10, pady=10)

        global bouton4
        bouton4 = tk.Button(self, text="Afficher")
        bouton4["command"] = lambda: afficher_texte(champ_texte4)
        bouton4.grid(row=7, column=1, padx=10, pady=10)

        liste_des_canvas.append((label4, label4.grid_info()))
        liste_des_canvas.append((champ_texte4, champ_texte4.grid_info()))
        liste_des_canvas.append((bouton4, bouton4.grid_info()))
        # =================================================== #

        # =================================================== #
        # TEMPLATE TITRE + CHAMP + BOUTTON A REPETER A LENVIE #
        label5 = tk.Label(self, text="Immatriculation :")
        label5.grid(row=8, column=0, padx=10, pady=10, sticky="w")

        global champ_texte5
        champ_texte5 = tk.Entry(self)
        champ_texte5.grid(row=9, column=0, padx=10, pady=10)

        bouton5 = tk.Button(self, text="Afficher")
        bouton5["command"] = lambda: afficher_texte(champ_texte5)
        bouton5.grid(row=9, column=1, padx=10, pady=10)

        liste_des_canvas.append((label5, label5.grid_info()))
        liste_des_canvas.append((champ_texte5, champ_texte5.grid_info()))
        liste_des_canvas.append((bouton5, bouton5.grid_info()))
        # =================================================== #

        # =================================================== #
        # =========== NE PAS DUPLIQUER ====================== #
        liste_des_pages.append(liste_des_canvas)
        liste_des_images.append((None))
        # =========== CODE QUI GENERE LES PAGES ============= #
        # =================================================== #


        widgets = {
            "rapport_title": champ_texte,
            "rapport_date": champ_texte2,
            "agency_name": champ_texte3,
            "boat_name": champ_texte4,
            "boat_imm": champ_texte5
        }

        bouton_suivant = tk.Button(self, text="Suivant")
        bouton_suivant["command"] = lambda: self.change_page('n')
        bouton_suivant.grid(row=100, column=3, padx=10, pady=10)

        bouton_precedent = tk.Button(self, text="Générer le rapport")
        bouton_precedent["command"] = lambda: self.compile_to_pdf()
        bouton_precedent.grid(row=100, column=1, padx=10, pady=10)

        bouton_precedent = tk.Button(self, text="Précédent")
        bouton_precedent["command"] = lambda: self.change_page('p')
        bouton_precedent.grid(row=100, column=0, padx=10, pady=10, sticky="w")

    def afficher_texte(champ):
        contenu = champ.get()
        print(contenu)

    def hide_page(self, number_of_the_page):
        page = liste_des_pages[number_of_the_page]
        for (canvas, opt) in page:
            canvas.grid_forget()

    def show_page(self, number_of_the_page):
        if (len(liste_des_pages) <= number_of_the_page):
            self.create_new_expertise_page()
            return

        page = liste_des_pages[number_of_the_page]
        for (canvas, opt) in page:
            canvas.grid(opt)

    def change_page(self, next_or_prev):
        global actual_page_number
        if actual_page_number == 0 and next_or_prev == 'p':
            return

        self.hide_page(actual_page_number)
        if (next_or_prev == 'n'):
            actual_page_number += 1
            self.show_page(actual_page_number)
        else:
            actual_page_number -= 1
            self.show_page(actual_page_number)

        self.update_idletasks()

    def replace_in_file_with_key(self, key, replace_content):
        with fileinput.FileInput('rapport.tex', inplace = True, backup ='.bak') as f:
            for line in f:
                if(key in line):
                    print(line.replace(key, replace_content), end ='')
                else:
                    print(line, end ='')

    def write_in_file(filename, content):
        with open(filename, "w") as file:
            # Write the content to the file
            file.write(content)

    def CompileLaTeXToPDF(self):
        subprocess.run(["pdflatex", 'rapport.tex'])

    def LaTeXifier(self, array_of_info):
        shutil.copyfile(template_file, 'rapport.tex')
        for data in array_of_info:
            for info in data:
                print("=========================")
                print(info)
                print("=========================")
        file_name = 'rapport.tex'
        new_line  = '\\title{' + champ_texte.get() + '}\n'
        n = 23

        # Lire le contenu du fichier dans une liste
        with open(file_name, "r") as file:
            lines = file.readlines()

        lines[n - 1] = new_line

        # Insérer la nouvelle ligne à la position n - 1
        # lines.insert(n - 1, new_line)

        with open(file_name, "w") as file:
            file.writelines(lines)

        self.replace_in_file_with_key('XI_DATE_EX', champ_texte2.get())
        self.replace_in_file_with_key('XI_MAC_EX', champ_texte3.get())
        self.replace_in_file_with_key('XI_SHIP_NAME_EX', champ_texte4.get())
        self.replace_in_file_with_key('XI_SHIP_IMM_EX', champ_texte5.get())
        self.CompileLaTeXToPDF()


    def compile_to_pdf(self):
        result = []
        for page in liste_des_pages:
            temp = []
            for (canva, opt) in page:
                if (isinstance(canva, tk.Entry)):
                    if (canva.get() != ''):
                        temp.append(canva.get())
            if (temp != []):
                result.append(temp)
        print(result)
        print('le rapport a été compilé :)')
        self.LaTeXifier(result)

    def modifier_champ_etat(self, etat, field):
        if (etat == 'c'):
            field["text"] = 'état critique'
            field["bg"] = 'AntiqueWhite2'
            field["fg"] = 'red'
        if (etat == 'g'):
            field["text"] = 'état grave'
            field["bg"] = 'AntiqueWhite2'
            field["fg"] = 'orange'
        if (etat == 'm'):
            field["text"] = 'état moyen'
            field["bg"] = 'AntiqueWhite2'
            field["fg"] = 'yellow'
        if (etat == 'b'):
            field["text"] = 'bon état'
            field["bg"] = 'AntiqueWhite2'
            field["fg"] = 'green'

    def create_new_expertise_page(self):
        liste_des_canvas = []

        label = tk.Label(self, text="Partie du bateau :")
        label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        champ_texte = tk.Entry(self)
        champ_texte.grid(row=1, column=0, padx=10, pady=10)

        bouton = tk.Button(self, text="Afficher")
        bouton["command"] = lambda: afficher_texte(champ_texte)
        bouton.grid(row=1, column=1, padx=10, pady=10)

        add_picture_buton = tk.Button(self, text="Joindre Photo 1", command=lambda: self.show_modal(1))
        add_picture_buton.grid(row=0, column=4, padx=10, pady=10)

        add_picture_buton2 = tk.Button(self, text="Joindre Photo 2", command=lambda: self.show_modal(2))
        add_picture_buton2.grid(row=1, column=4, padx=10, pady=10)

        label2 = tk.Label(self, text="Etat de la partie")
        label2.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        champ_etat = tk.Label(self, text="")
        champ_etat.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        bouton11 = tk.Button(self, text="Critique")
        bouton11["command"] = lambda: self.modifier_champ_etat('c', champ_etat)
        bouton11.grid(row=9, column=0, padx=0, pady=0, sticky="", ipadx=20)

        bouton12 = tk.Button(self, text="Grave")
        bouton12["command"] = lambda: self.modifier_champ_etat('g', champ_etat)
        bouton12.grid(row=9, column=1, padx=1, pady=0, sticky="", columnspan=1, ipadx=20)

        bouton13 = tk.Button(self, text="Moyen")
        bouton13["command"] = lambda: self.modifier_champ_etat('m', champ_etat)
        bouton13.grid(row=9, column=2, padx=0, pady=10, sticky="", columnspan=1, ipadx=20)

        bouton14 = tk.Button(self, text="Bon")
        bouton14["command"] = lambda: self.modifier_champ_etat('b', champ_etat)
        bouton14.grid(row=9, column=3, padx=0, pady=0, sticky="", columnspan=2, ipadx=20)

        label22 = tk.Label(self, text="")
        label22.grid(row=10, column=0, padx=10, pady=10, sticky="w", columnspan=2)    

        liste_des_canvas.append((label, label.grid_info()))
        liste_des_canvas.append((champ_texte, champ_texte.grid_info()))
        liste_des_canvas.append((bouton, bouton.grid_info()))

        liste_des_canvas.append((label2, label2.grid_info()))

        liste_des_canvas.append((bouton11, bouton11.grid_info()))
        liste_des_canvas.append((bouton12, bouton12.grid_info()))
        liste_des_canvas.append((bouton13, bouton13.grid_info()))
        liste_des_canvas.append((bouton14, bouton14.grid_info()))
        liste_des_canvas.append((champ_etat, champ_etat.grid_info()))

        liste_des_pages.append(liste_des_canvas)
        liste_des_images.append((None, None))

    def display_image(self, image_path, x, y):
        # Ouvrir l'image à l'aide de la bibliothèque PIL
        if (image_path != None):
            image = Image.open(image_path)
            # Convertir l'image en PhotoImage
            photo = ImageTk.PhotoImage(image)

            # Créer un widget Label pour afficher l'image
            label = tk.Label(self, image=photo)
            label.image = photo  # Conserver une référence à l'image pour éviter la suppression par le garbage collector
            label.grid(row=x, column=y)  # Positionner l'image aux coordonnées (x, y)
            # label.grid(row=0, column=0, padx=10, pady=10, sticky="w") #
            liste_des_pages[actual_page_number].append((label, label.grid_info()))


# =================================================== #
#            PARTIE OUVRANT LA MODALE PhotoImage      #
# =================================================== #
    def show_modal(self, image_number):
        image_resizer_modal = ImageResizerModal(self)
        image_resizer_modal.grab_set()
        self.wait_window(image_resizer_modal)  # Attendez que la fenêtre modale soit fermée
        saved_image_path = image_resizer_modal.get_saved_image_path()  # Récupérez la valeur de retour
        print(f"Image sauvegardée: {saved_image_path}")
        self.display_image(saved_image_path, 10, image_number)
        # Convertir le tuple en liste
        temp_list = list(liste_des_images[actual_page_number])

        # Modifier l'élément à la position image_number
        temp_list[image_number] = saved_image_path

        # Reconvertir la liste en tuple et l'assigner à la position actual_page_number
        liste_des_images[actual_page_number] = tuple(temp_list)
        return saved_image_path
# =================================================== #


if __name__ == "__main__":
    app = YourMainApp()
    app.mainloop()
