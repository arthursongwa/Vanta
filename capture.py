import tkinter as tk
from PIL import ImageGrab
from datetime import datetime
import os

IMAGES_DIR = "images"
os.makedirs(IMAGES_DIR, exist_ok=True)

def capture_zone_personnalisee(nom_base="capture"):

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)  # transparence
    root.configure(bg='black')
    root.title("Sélectionne une zone")

    canvas = tk.Canvas(root, cursor="cross", bg="gray", highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)

    start_x = start_y = rect_id = None

    def on_mouse_down(event):
        nonlocal start_x, start_y, rect_id
        start_x, start_y = event.x, event.y
        rect_id = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="red", width=2)

    def on_mouse_drag(event):
        nonlocal rect_id
        canvas.coords(rect_id, start_x, start_y, event.x, event.y)

    def on_mouse_up(event):
        root.destroy()

        # Déterminer les coordonnées exactes
        x1 = min(start_x, event.x)
        y1 = min(start_y, event.y)
        x2 = max(start_x, event.x)
        y2 = max(start_y, event.y)

        # Capturer la zone de l'écran
        img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        path = os.path.join(IMAGES_DIR, f"{nom_base}_{datetime.now().strftime('%H%M%S')}.png")
        img.save(path)
        print(f"📸 Capture enregistrée : {path}")
        root.quit()
        root.path_capture = path

    canvas.bind("<ButtonPress-1>", on_mouse_down)
    canvas.bind("<B1-Motion>", on_mouse_drag)
    canvas.bind("<ButtonRelease-1>", on_mouse_up)

    root.mainloop()

    return getattr(root, "path_capture", None)
