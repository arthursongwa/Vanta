import pyautogui
import time

print("⌛ Démarrage dans 3 secondes...")
time.sleep(1)
# pyautogui.scroll(-300)
nbr = 0
N = 1

for i in range(N):  # Nombre de scrolls que tu souhaites
    print(f"\n🔁 Tentative {i+1} sur {N}")

    # print("🔎 Recherche du contexte...")
    
    position = pyautogui.locateOnScreen("images\\contexte.PNG", confidence=0.8)

    if position:
        print("✅ Contexte détecté")

        # print("🔍 Recherche de l'offre...")
        try:
            position = pyautogui.locateCenterOnScreen("images\\Capture.PNG", confidence=0.4)
        except:
            print("on continue: offre")

        if position:
            # print("✅ Offre trouvée, clic en cours...")
            try:
                pyautogui.click(position, button="right")
                time.sleep(0.4)
                position = pyautogui.locateCenterOnScreen("images\\open.PNG", confidence=0.6)
                pyautogui.click(position, button="left")
                time.sleep(3)
            except:
                print("Erreur ouverture de loffre")

            # print("📩 Tentative de postulation...1")
            try:
                pyautogui.scroll(-300)
                time.sleep(0.5)
                pos = pyautogui.locateCenterOnScreen("images\\postule.PNG", confidence=0.6)
                pyautogui.click(pos, button="left")
                print("✅ Postulation effectuée")
                time.sleep(2)
            except:
                print("on continue: postulation1")
            
            # print("📩 Tentative de postulation...2")
            try:
                pyautogui.scroll(-200)
                pos = pyautogui.locateCenterOnScreen("images\\postule2.PNG", confidence=0.8)
                pyautogui.click(pos, button="left")
                print("✅ Postulation effectuée")
                time.sleep(3)
                nbr += 1
            except:
                print("on continue: postulation2")

            print("❌ Fermeture de la fenêtre...")
            try:
                pos = pyautogui.locateCenterOnScreen("images\\ferme.PNG", confidence=0.8)
                pyautogui.click(pos)
                time.sleep(2)
                print("✅ Page fermée")
            except:
                print("on continue: Fermeture")
            
            print("🔽 Scroll vers le bas et clic pour continuer...")
            pyautogui.moveTo(50, 500)
            pyautogui.scroll(-280)

        else:
            print("❌ Offre non trouvée")
    else:
        print("❌ Contexte non détecté")

print("Nbr candidater "+str(nbr))