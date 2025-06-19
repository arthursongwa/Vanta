import pyautogui
import time
import json

actions = []  # Liste pour stocker les actions

def est_visible(image_path):
    try:
        position = pyautogui.locateOnScreen(image_path, confidence=0.8)
        return position is not None
    except Exception as e:
        print(f"⚠️ Erreur lors de la vérification du contexte : {e}")
        return False

def executer_action(action):
    try:
        # S'il y a une condition de contexte, on la vérifie
        if "contexte" in action:
            if not est_visible(action["contexte"]):
                print(f"⛔ Contexte non détecté : {action['contexte']}, action ignorée.")
                return
            else:
                print(f"🟢 Contexte détecté : {action['contexte']}")

        # Rechercher l'élément cible
        position = pyautogui.locateCenterOnScreen(action["image_cible"], confidence=0.8)
        if position:
            print(f"✅ Élément trouvé : {action['image_cible']} à {position}")
            pyautogui.click(position)
            time.sleep(0.3)
            if action["type"] == "Saisie":
                pyautogui.write(action["texte"], interval=0.05)
            elif action["type"] == "Scroll":
                pyautogui.scroll(int(action["texte"])*-1)
        else:
            print(f"❌ Élément non trouvé : {action['image_cible']}")

    except Exception as e:
        print(f"⚠️ Erreur sur l'action '{action.get('image_cible', 'inconnue')}' : {e}")

def boucle_automatisation(stop_flag=None, nbr=3, on_progress=None):
    with open("actions.json", "r") as f:
        actions = json.load(f)

    # Délai pour te laisser le temps de préparer l'écran
    time.sleep(3)
    for i in range(nbr):
        if stop_flag():
            print("🛑 Exécution stoppée par l'utilisateur.")
            return -1

        print(f"\n🔁 Itération {i+1}/{nbr}...")
        for action in actions:
            if stop_flag and stop_flag():
                print("🛑 Interruption pendant l'exécution des actions.")
                return -1
            executer_action(action)
            if action["delais"] != "Delai" or action["delais"] != "Delais":
                time.sleep(int(action["delais"]))

        print(f"{round((i + 1) * 100 / nbr)}% effectués.")
        
        if on_progress:
            on_progress(round((i + 1) * 100 / nbr))
        time.sleep(1)

    print("✅ Automatisation terminée.")
