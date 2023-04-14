import tkinter as tk
import subprocess
import shutil
import fileinput
from PIL import ImageTk, Image
from tkinter import PhotoImage

template_file = 'template_file.tex'
output_file = 'rapport.tex'

liste_des_pages = []
liste_des_canvas = []

actual_page_number = 0

def afficher_texte(champ):
    contenu = champ.get()
    print(contenu)

def hide_page(number_of_the_page):
    page = liste_des_pages[number_of_the_page]
    for (canvas, opt) in page:
        canvas.grid_forget()

def show_page(number_of_the_page):
    if (len(liste_des_pages) <= number_of_the_page):
        create_new_expertise_page()
        return

    page = liste_des_pages[number_of_the_page]
    for (canvas, opt) in page:
        canvas.grid(opt)

def change_page(next_or_prev):
    global actual_page_number
    if actual_page_number == 0 and next_or_prev == 'p':
        return

    hide_page(actual_page_number)
    if (next_or_prev == 'n'):
        actual_page_number += 1
        show_page(actual_page_number)
    else:
        actual_page_number -= 1
        show_page(actual_page_number)

    fenetre.update_idletasks()

def replace_in_file_with_key(key, replace_content):
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

def CompileLaTeXToPDF():
    subprocess.run(["pdflatex", 'rapport.tex'])

def LaTeXifier(array_of_info):
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

    replace_in_file_with_key('XI_DATE_EX', champ_texte2.get())
    replace_in_file_with_key('XI_MAC_EX', champ_texte3.get())
    replace_in_file_with_key('XI_SHIP_NAME_EX', champ_texte4.get())
    CompileLaTeXToPDF()


def compile_to_pdf():
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
    LaTeXifier(result)

# =================================================== #
# Création de la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Exemple avec label, champ de texte et bouton")
# =================================================== #


# =================================================== #
# Création et placement du label
label = tk.Label(fenetre, text="Titre du rapport :")
label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Création et placement du champ de texte
champ_texte = tk.Entry(fenetre)
champ_texte.grid(row=1, column=0, padx=10, pady=10)

# Création et placement du bouton
bouton = tk.Button(fenetre, text="Afficher")
bouton["command"] = lambda: afficher_texte(champ_texte)
bouton.grid(row=1, column=1, padx=10, pady=10)

liste_des_canvas.append((label, label.grid_info()))
liste_des_canvas.append((champ_texte, champ_texte.grid_info()))
liste_des_canvas.append((bouton, bouton.grid_info()))
# =================================================== #

# =================================================== #
# TEMPLATE TITRE + CHAMP + BOUTTON A REPETER A LENVIE #
label2 = tk.Label(fenetre, text="Date de l'expertise :")
label2.grid(row=2, column=0, padx=10, pady=10, sticky="w")

champ_texte2 = tk.Entry(fenetre)
champ_texte2.grid(row=3, column=0, padx=10, pady=10)

bouton2 = tk.Button(fenetre, text="Afficher")
bouton2["command"] = lambda: afficher_texte(champ_texte2)
bouton2.grid(row=3, column=1, padx=10, pady=10)

liste_des_canvas.append((label2, label2.grid_info()))
liste_des_canvas.append((champ_texte2, champ_texte2.grid_info()))
liste_des_canvas.append((bouton2, bouton2.grid_info()))
# =================================================== #

# =================================================== #
# TEMPLATE TITRE + CHAMP + BOUTTON A REPETER A LENVIE #
label3 = tk.Label(fenetre, text="Nom du cabinet :")
label3.grid(row=4, column=0, padx=10, pady=10, sticky="w")

champ_texte3 = tk.Entry(fenetre)
champ_texte3.grid(row=5, column=0, padx=10, pady=10)

bouton3 = tk.Button(fenetre, text="Afficher")
bouton3["command"] = lambda: afficher_texte(champ_texte3)
bouton3.grid(row=5, column=1, padx=10, pady=10)

liste_des_canvas.append((label3, label3.grid_info()))
liste_des_canvas.append((champ_texte3, champ_texte3.grid_info()))
liste_des_canvas.append((bouton3, bouton3.grid_info()))
# =================================================== #

# =================================================== #
# TEMPLATE TITRE + CHAMP + BOUTTON A REPETER A LENVIE #
label4 = tk.Label(fenetre, text="Nom du navire :")
label4.grid(row=6, column=0, padx=10, pady=10, sticky="w")

champ_texte4 = tk.Entry(fenetre)
champ_texte4.grid(row=7, column=0, padx=10, pady=10)

bouton4 = tk.Button(fenetre, text="Afficher")
bouton4["command"] = lambda: afficher_texte(champ_texte4)
bouton4.grid(row=7, column=1, padx=10, pady=10)

liste_des_canvas.append((label4, label4.grid_info()))
liste_des_canvas.append((champ_texte4, champ_texte4.grid_info()))
liste_des_canvas.append((bouton4, bouton4.grid_info()))
# =================================================== #

# =================================================== #
# =========== NE PAS DUPLIQUER ====================== #
liste_des_pages.append(liste_des_canvas)
# =========== CODE QUI GENERE LES PAGES ============= #
# =================================================== #


widgets = {
    "rapport_title": champ_texte,
    "rapport_date": champ_texte2,
    "agency_name": champ_texte3
}

bouton_suivant = tk.Button(fenetre, text="Suivant")
bouton_suivant["command"] = lambda: change_page('n')
bouton_suivant.grid(row=100, column=3, padx=10, pady=10)

bouton_precedent = tk.Button(fenetre, text="Générer le rapport")
bouton_precedent["command"] = lambda: compile_to_pdf()
bouton_precedent.grid(row=100, column=1, padx=10, pady=10)

bouton_precedent = tk.Button(fenetre, text="Précédent")
bouton_precedent["command"] = lambda: change_page('p')
bouton_precedent.grid(row=100, column=0, padx=10, pady=10, sticky="w")


#    im = Image.open("fleur.jpg")
 #   img = im.resize((450, 350))
  #  img = ImageTk.PhotoImage(img)
   # label_image = tk.Label(fenetre, image=img)
    #label_image.grid(row=1, column=1, padx=10, pady=10)

def modifier_champ_etat(etat, field):
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

def create_new_expertise_page():
    liste_des_canvas = []

    label = tk.Label(fenetre, text="Partie du bateau :")
    label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    champ_texte = tk.Entry(fenetre)
    champ_texte.grid(row=1, column=0, padx=10, pady=10)

    bouton = tk.Button(fenetre, text="Afficher")
    bouton["command"] = lambda: afficher_texte(champ_texte)
    bouton.grid(row=1, column=1, padx=10, pady=10)

    label2 = tk.Label(fenetre, text="Etat de la partie")
    label2.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    champ_etat = tk.Label(fenetre, text="")
    champ_etat.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    bouton11 = tk.Button(fenetre, text="Critique")
    bouton11["command"] = lambda: modifier_champ_etat('c', champ_etat)
    bouton11.grid(row=9, column=0, padx=0, pady=0, sticky="")

    bouton12 = tk.Button(fenetre, text="Grave")
    bouton12["command"] = lambda: modifier_champ_etat('g', champ_etat)
    bouton12.grid(row=9, column=1, padx=1, pady=0, sticky="", columnspan=1)

    bouton13 = tk.Button(fenetre, text="Moyen")
    bouton13["command"] = lambda: modifier_champ_etat('m', champ_etat)
    bouton13.grid(row=9, column=2, padx=0, pady=10, sticky="", columnspan=1)

    bouton14 = tk.Button(fenetre, text="Bon")
    bouton14["command"] = lambda: modifier_champ_etat('b', champ_etat)
    bouton14.grid(row=9, column=3, padx=0, pady=0, sticky="", columnspan=2)

    label22 = tk.Label(fenetre, text="")
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


# Lancement de la boucle principale
fenetre.mainloop()
