import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from capture import capture_zone_personnalisee
from automate import boucle_automatisation
import threading

actions = []
execution_thread = None
stop_execution = False
execution_en_cours = False

IMAGES_DIR = "images"
os.makedirs(IMAGES_DIR, exist_ok=True)

def capturer_image_cible():
    path = capture_zone_personnalisee("cible")
    if path:
        entry_image_cible.delete(0, tk.END)
        entry_image_cible.insert(0, path)

def capturer_image_contexte():
    path = capture_zone_personnalisee("contexte")
    if path:
        entry_image_contexte.delete(0, tk.END)
        entry_image_contexte.insert(0, path)

def ajouter_action():
    image_cible = entry_image_cible.get().strip()
    image_contexte = entry_image_contexte.get().strip()
    action_type = type_var.get()
    valeur = entry_valeur.get().strip()

    if not image_cible:
        messagebox.showerror("Erreur", "Tu dois définir une image cible.")
        return

    action = {
        "image_cible": image_cible,
        "type": action_type
    }

    if image_contexte:
        action["contexte"] = image_contexte

    if action_type == "Saisie":
        if not valeur:
            messagebox.showerror("Erreur", "Tu dois entrer une valeur pour la saisie.")
            return
        action["texte"] = valeur

    actions.append(action)
    sauvegarder_actions()
    rafraichir_liste()
    vider_champs()

def supprimer_action():
    selection = listbox_actions.curselection()
    if selection:
        index = selection[0]
        del actions[index]
        sauvegarder_actions()
        rafraichir_liste()

def sauvegarder_actions():
    with open("actions.json", "w") as f:
        json.dump(actions, f, indent=2)

def vider_champs():
    entry_image_cible.delete(0, tk.END)
    entry_image_contexte.delete(0, tk.END)
    entry_valeur.delete(0, tk.END)

def toggle_execution():
    global execution_en_cours, execution_thread, stop_execution

    if not execution_en_cours:
        execution_en_cours = True
        stop_execution = False
        btn_exec.configure(text="⛔ Stop", bg="#dc3545", fg="white")

        def stop_flag():
            return stop_execution

        def run():
            boucle_automatisation(stop_flag, 5)
            execution_en_cours = False
            btn_exec.configure(text="▶️ Exécuter", bg="#007bff", fg="white")

        execution_thread = threading.Thread(target=run)
        execution_thread.start()

    else:
        stop_execution = True
        execution_en_cours = False
        btn_exec.configure(text="▶️ Exécuter", bg="#007bff", fg="white")

def rafraichir_liste():
    listbox_actions.delete(0, tk.END)
    for i, action in enumerate(actions, 1):
        label = f"{i}. {action['type']} sur {os.path.basename(action['image_cible'])}"
        listbox_actions.insert(tk.END, label)

def swap_actions(index1, index2):
    if 0 <= index1 < len(actions) and 0 <= index2 < len(actions):
        actions[index1], actions[index2] = actions[index2], actions[index1]
        sauvegarder_actions()
        rafraichir_liste()
        listbox_actions.selection_set(index2)
def creer_bouton_arret_flottant():
    stop_window = tk.Toplevel(root)
    stop_window.overrideredirect(True)  # Supprime la bordure/fenêtre
    stop_window.attributes('-topmost', True)  # Toujours au-dessus
    stop_window.configure(bg="#dc3545")  # rouge comme le bouton


    # Taille et position : en bas à droite
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    width, height = 50, 50
    x = screen_width - width - 20
    y = screen_height - height - 60
    stop_window.geometry(f"{width}x{height}+{x}+{y}")

    # Bouton ❌
    btn_stop = tk.Button(stop_window, text="❌", bg="#dc3545", fg="white",
                         font=("Arial", 16, "bold"), relief="flat", borderwidth=0,
                         command=forcestop)
    btn_stop.pack(expand=True, fill="both")

    # Déplace avec la souris (facultatif)
    def start_move(event): stop_window.x = event.x; stop_window.y = event.y
    def stop_move(event): pass
    def do_move(event):
        x = event.x_root - stop_window.x
        y = event.y_root - stop_window.y
        stop_window.geometry(f"+{x}+{y}")
    stop_window.bind("<ButtonPress-1>", start_move)
    stop_window.bind("<B1-Motion>", do_move)

def forcestop():
    global stop_execution, execution_en_cours
    stop_execution = True
    execution_en_cours = False
    btn_exec.configure(text="▶️ Exécuter", bg="#007bff", fg="white")

def creer_bordure_interrompue():
    bordures = []
    largeur = root.winfo_screenwidth()
    hauteur = root.winfo_screenheight()
    epaisseur = 4  # épaisseur des traits
    longueur_trait = 20  # longueur de chaque trait
    espace = 15          # espace entre les traits

    def create_trait(x, y, w, h):
        b = tk.Toplevel(root)
        b.overrideredirect(True)
        b.attributes('-topmost', True)
        b.geometry(f"{w}x{h}+{x}+{y}")
        b.configure(bg="red")
        return b

    # Création des traits horizontaux (haut et bas)
    x = 0
    while x < largeur:
        # Haut
        bordures.append(create_trait(x, 0, min(longueur_trait, largeur - x), epaisseur))
        # Bas
        bordures.append(create_trait(x, hauteur - epaisseur, min(longueur_trait, largeur - x), epaisseur))
        x += longueur_trait + espace

    # Création des traits verticaux (gauche et droite)
    y = 0
    while y < hauteur:
        # Gauche
        bordures.append(create_trait(0, y, epaisseur, min(longueur_trait, hauteur - y)))
        # Droite
        bordures.append(create_trait(largeur - epaisseur, y, epaisseur, min(longueur_trait, hauteur - y)))
        y += longueur_trait + espace

    def clignoter():
        for b in bordures:
            couleur = b.cget("bg")
            b.configure(bg="red" if couleur != "red" else "black")
        root.after(500, clignoter)

    clignoter()
    root.bordures_clignotantes = bordures

# Fenêtre principale
root = tk.Tk()
root.title("Créateur d'automatisation")
root.configure(bg="#f0f0f0")

# Champs d'action
tk.Label(root, text="📌 Image cible", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
entry_image_cible = tk.Entry(root, width=50)
entry_image_cible.grid(row=0, column=1)
tk.Button(root, text="Capturer", command=capturer_image_cible).grid(row=0, column=2)

tk.Label(root, text="🧠 Contexte (optionnel)", bg="#f0f0f0").grid(row=1, column=0, sticky="w")
entry_image_contexte = tk.Entry(root, width=50)
entry_image_contexte.grid(row=1, column=1)
tk.Button(root, text="Capturer", command=capturer_image_contexte).grid(row=1, column=2)

tk.Label(root, text="⚙️ Type d'action", bg="#f0f0f0").grid(row=2, column=0, sticky="w")
type_var = tk.StringVar(value="Click")
tk.OptionMenu(root, type_var, "Click", "Saisie").grid(row=2, column=1, sticky="w")

tk.Label(root, text="📝 Valeur (si Saisie)", bg="#f0f0f0").grid(row=3, column=0, sticky="w")
entry_valeur = tk.Entry(root, width=50)
entry_valeur.grid(row=3, column=1)

# Boutons de contrôle
frame_btn = tk.Frame(root, bg="#f0f0f0")
frame_btn.grid(row=4, column=0, columnspan=3, pady=10)
tk.Button(frame_btn, text="➕ Ajouter", bg="#28a745", fg="white", command=ajouter_action).pack(side="left", padx=5)
btn_exec = tk.Button(frame_btn, text="▶️ Exécuter", bg="#007bff", fg="white", command=toggle_execution)
btn_exec.pack(side="left", padx=5)
tk.Button(frame_btn, text="🗑 Supprimer", bg="#ffc107", command=supprimer_action).pack(side="left", padx=5)

# Liste des actions
listbox_actions = tk.Listbox(root, width=70, height=15, selectbackground="#007bff")
listbox_actions.grid(row=5, column=0, columnspan=3, pady=10)

# Réorganisation avec flèches
frame_order = tk.Frame(root, bg="#f0f0f0")
frame_order.grid(row=6, column=0, columnspan=3)
tk.Button(frame_order, text="🔼 Monter", command=lambda: swap_actions(listbox_actions.curselection()[0], listbox_actions.curselection()[0] - 1)).pack(side="left", padx=10)
tk.Button(frame_order, text="🔽 Descendre", command=lambda: swap_actions(listbox_actions.curselection()[0], listbox_actions.curselection()[0] + 1)).pack(side="left", padx=10)

# Charger les actions si elles existent
def charger_actions():
    global actions
    if os.path.exists("actions.json"):
        with open("actions.json", "r") as f:
            actions = json.load(f)
        rafraichir_liste()

charger_actions()
root.mainloop()