import pyautogui
import time

print("⌛ Démarrage dans 3 secondes...")
time.sleep(3)

for i in range(10):  # Nombre de scrolls que tu souhaites
    print(f"\n🔁 Tentative {i+1} sur 10")

    print("🔎 Recherche du contexte...")
    try:
        position = pyautogui.locateOnScreen("images\\contexte.PNG", confidence=0.8)
    except:
        print("on continue: contexte")

    if position:
        print("✅ Contexte détecté")

        print("🔍 Recherche de l'offre...")
        try:
            position = pyautogui.locateCenterOnScreen("images\\Capture.PNG", confidence=0.8)
        except:
            print("on continue: offre")

        if position:
            print("✅ Offre trouvée, clic en cours...")
            pyautogui.click(position)
            time.sleep(3)

            print("📩 Tentative de postulation...")
            try:
                pos = pyautogui.locateCenterOnScreen("images\\postule.PNG", confidence=0.8)
                pyautogui.click(pos)
                print("✅ Postulation effectuée")
                time.sleep(3)
            except:
                print("on continue: postulation")

            print("❌ Fermeture de la fenêtre...")
            try:
                pos = pyautogui.locateCenterOnScreen("images\\ferme.PNG", confidence=0.8)
                pyautogui.click(pos)
                time.sleep(3)
                print("✅ Page fermée")
            except:
                print("on continue: Fermeture")

            print("🔽 Scroll vers le bas et clic pour continuer...")
            try:
                pos = pyautogui.locateCenterOnScreen("images\\click.PNG", confidence=0.8)
                pyautogui.click(pos)
                pyautogui.scroll(-300)
                print("✅ Scroll effectué")
                time.sleep(2)  # Pause pour que la page charge
            except:
                print("on continue: click")

        else:
            print("❌ Offre non trouvée")
    else:
        print("❌ Contexte non détecté")

