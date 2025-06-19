from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QScrollArea, QFrame, QSpinBox, QProgressBar, QLineEdit, QComboBox
)
from PyQt5.QtCore import Qt,  QTimer, QSize
from PyQt5.QtGui import QPainter, QPen, QIcon
import sys, os, json

from sympy import true
from capture import capture_zone_personnalisee
from automate import boucle_automatisation
import threading

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vanta")
        self.setFixedSize(700, 700)
        self.setStyleSheet("background-color: #262626; color: white; font-family: Inter;")
    
        self.label_log = QLabel("Log")
        self.label_log.setStyleSheet("font-size: 16px; font-weight: 300;")

        self.actions = []
        self.charger_actions()
        self.progressValue = 0
                
        self.execution_thread = None
        self.stop_execution = False
        self.execution_en_cours = False

        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)

        # ========== TOP CONTROL AREA ==========
        control_layout = QHBoxLayout()
        control_layout.setContentsMargins(0, 0, 20, 0)

        label_nbr = QLabel("Nbr")
        label_nbr.setStyleSheet("font-size: 20px; font-weight: 500; padding: 20px 0 20px 20px;")
        self.spinbox = QSpinBox()
        self.spinbox.setRange(1, 99)
        self.spinbox.setValue(2)
        self.spinbox.setStyleSheet("""
            QSpinBox {
                background-color: #262626;
                font-size: 20px;
                padding: 10px;
                color: white;
                border-top-left-radius: 5px;
                border-top-right-radius: 0;
                border-bottom-left-radius: 5px;
                border-bottom-right-radius: 0;
            }
        """)

        control_layout.addWidget(label_nbr)
        control_layout.addWidget(self.spinbox)
        control_layout.addStretch()
        control_layout.addWidget(self.label_log)

        # ========== BUTTONS ==========
        button_layout = QHBoxLayout()
        self.start_btn = QPushButton("START")
        self.start_btn.clicked.connect(self.toggle_execution)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #3B82F6;
                font-size: 20px;
                padding: 10px 15px;
                border-top-left-radius: 0;
                border-top-right-radius: 10px;
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 0;
            }
            QPushButton:hover{
            background-color: #426DB4;}
        """)
        self.add_btn = QPushButton("+ ADD")
        self.add_btn.clicked.connect(self.afficher_formulaire)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #16A34A;
                font-size: 20px;
                padding: 10px 15px;
                border-top-left-radius: 10px;
                border-top-right-radius: 0;
                border-bottom-left-radius: 0;
                border-bottom-right-radius: 10px;
            }
            QPushButton:hover{background-color: #2AD268;} 
        """)

        button_layout.addWidget(self.start_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.add_btn)
        
        # ========== FORMULAIRE MASQUÉ PAR DÉFAUT ==========
        self.form_widget = QWidget()
        form_layout = QVBoxLayout()

        # ========== LIGNE 1 ==========
        ligne1_layout = QHBoxLayout()

        self.combo_box = QComboBox()
        self.combo_box.addItems(["Type d'action...", "Click", "Saisie", "Scroll"])
        self.combo_box.setStyleSheet("""QComboBox {
            background-color: #1F1F1F;
            color: white;
            padding: 8px;
            font-size: 18px;
            border: 1px solid #555;
            border-radius: 6px;
        }
        QComboBox QAbstractItemView {
            background-color: #2C2C2C;
            selection-background-color: #3B82F6;
        }""")
        self.combo_box.currentTextChanged.connect(self.afficher_input_saisie)

        self.delay = QComboBox()
        self.delay.addItems(["Delais", "0s", "1s", "2s", "3s", "5s"])
        self.delay.setStyleSheet(self.combo_box.styleSheet())

        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("Valeur à saisir...")
        self.input_line.setStyleSheet("""QLineEdit {
            background-color: #1F1F1F;
            color: white;
            padding: 8px;
            font-size: 18px;
            border: 1px solid #555;
            border-radius: 6px;
        }""")
        self.input_line.hide()  # Masqué par défaut
 
        ligne1_layout.addWidget(self.combo_box)
        ligne1_layout.addWidget(self.delay)
        ligne1_layout.addWidget(self.input_line)

        # ========== LIGNE 2 ==========
        ligne2_layout = QHBoxLayout()

        self.cible = QPushButton("Cible")
        self.cible.clicked.connect(self.capturer_image_cible)
        self.cible.setStyleSheet("background-color: #3B82F6; color: white; padding: 8px 16px; border-radius: 6px;")

        self.contexte = QPushButton("Contexte")
        self.contexte.clicked.connect(self.capturer_image_contexte)
        self.contexte.setStyleSheet("background-color: #3B82F6; color: white; padding: 8px 16px; border-radius: 6px;")

        valider_btn = QPushButton("Valider")
        valider_btn.setStyleSheet("background-color: #3B82F6; color: white; padding: 8px 16px; border-radius: 6px;")
        valider_btn.clicked.connect(self.valider_formulaire)

        annuler_btn = QPushButton("Annuler")
        annuler_btn.setStyleSheet("background-color: #D01515; color: white; padding: 8px 16px; border-radius: 6px;")
        annuler_btn.clicked.connect(lambda: self.form_widget.hide())

        ligne2_layout.addWidget(self.cible)
        ligne2_layout.addWidget(self.contexte)
        ligne2_layout.addStretch()
        ligne2_layout.addWidget(valider_btn)
        ligne2_layout.addWidget(annuler_btn)

        # Assemblage final
        form_layout.addLayout(ligne1_layout)
        form_layout.addLayout(ligne2_layout)
        self.form_widget.setLayout(form_layout)
        self.form_widget.hide()

        # ========== SCROLLABLE AREA ==========
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none;")

        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignBottom)  # Pour afficher à partir du bas
        scroll.setWidget(scroll_content)

        # ========== CANVAS FRAME ==========
        canva = QFrame()
        canva.setStyleSheet("background-color: #1B1B1B; border-radius: 10px;")
        canva_layout = QVBoxLayout()
        canva_layout.setContentsMargins(0,0,0,0)
        canva_layout.addLayout(control_layout)
        canva_layout.addWidget(scroll)
        canva_layout.addLayout(button_layout)
        canva.setLayout(canva_layout)

        # ========== FINAL ASSEMBLY ==========
        main_layout.addWidget(canva)
        main_layout.addWidget(self.form_widget)
        self.setLayout(main_layout)

        for act in self.actions:
            self.ajouter_ligne_personnalisee(act['type'], act['texte'], act['delais'], act['image_cible'], act['contexte'], act)

    def afficher_input_saisie(self, texte):
        self.input_line.setVisible(texte == "Saisie" or texte == "Scroll")

    def print_log(self, message):
        self.label_log.setText(message)
        if "[ERROR]" in message:
            self.label_log.setStyleSheet("color: red; font-weight: bold;")
        elif "[WARN]" in message:
            self.label_log.setStyleSheet("color: orange; font-weight: bold;")
        else:
            self.label_log.setStyleSheet("color: #3B82F6; font-weight: normal;")
        print(message)
    
    def afficher_formulaire(self):
        self.print_log("[INFO] Affichage du formulaire...")
        self.input_line.clear()
        self.form_widget.show()

    def valider_formulaire(self):
        action = {
            'type': self.combo_box.currentText(),
            'texte': self.input_line.text().strip(),
            'delais': self.delay.currentText().replace("s",""),
            'image_cible': self.cible.text(),
            'contexte': self.contexte.text()
        }
        self.print_log(f"[DEBUG] Choix: {action['type']}, Texte: {action['texte']}, Délais: {action['delais']}, Cible: {action['image_cible']}, Contexte: {action['contexte']}")

        if action['contexte'] != "Contexte" and action['image_cible'] != "Cible":
            if action['type'] == "Click":
                self.actions.append(action)
                self.sauvegarder_actions()
                self.ajouter_ligne_personnalisee(action['type'], "", action['delais'], action['image_cible'], action['contexte'], action)
                self.form_widget.hide()
            elif (action['type'] == "Saisie" or action['type'] == "Scroll")and action['texte']:
                self.actions.append(action)
                self.sauvegarder_actions()
                self.ajouter_ligne_personnalisee(action['type'], action['texte'], action['delais'], action['image_cible'], action['contexte'], action)
                self.form_widget.hide()
            else:
                self.print_log("[WARN] Texte vide pour saisie")
        else:
            self.print_log("[ERROR] Contexte ou cible non défini")
        
    def ajouter_ligne_personnalisee(self, type, texte, delais, cible, contexte, action):
        type = type.lower()
        texte = texte.lower()
        self.print_log(f"[INFO] Ajout d'une action: {type}, texte: {texte}, delais: {delais}")
        line = QFrame()
        line.setFixedWidth(300)
        line.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 5px;
            }
            QLabel {
                color: #361818;
                font-size: 20px;
            }
            QPushButton {
                background-color: #D01515;
                color: white;
                border: none;
                font-size: 20px;
                border-radius: 4px;
                width: 40px;
                height: 40px;
            }
        """)
        line_layout = QHBoxLayout()

        icon = QPushButton()
        if type == "click": 
            icon.setIcon(QIcon("icons/click.svg")) 
        elif type == "saisie":
            icon.setIcon(QIcon("icons/write.svg"))
        elif type == "scroll":
            icon.setIcon(QIcon("icons/scroll.svg"))
        icon.setFixedSize(30, 30)
        icon.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: white;
            }
        """)

        line_layout.addWidget(icon)
        if type == "click": 
            line_layout.addWidget(QLabel("Click sur Button"))
        elif type == "saisie":
            line_layout.addWidget(QLabel("Saisie - "+texte))
        elif type == "scroll":
            line_layout.addWidget(QLabel("Scroll de "+texte+"px"))

        del_btn = QPushButton("-")
        del_btn.setFixedSize(40, 40)
        del_btn.clicked.connect(lambda: self.supprimer_action(line, action))

        line_layout.addWidget(del_btn)
        line.setLayout(line_layout)
        self.scroll_layout.addWidget(line, alignment=Qt.AlignCenter)

    def supprimer_action(self, line_widget, action_dict):
        if action_dict in self.actions:
            self.actions.remove(action_dict)
            self.print_log(f"Action supprimée : {action_dict}")
        else:
            self.print_log("Action non trouvée.")
        line_widget.deleteLater()
        self.sauvegarder_actions()

    def capturer_image_cible(self):
        path = capture_zone_personnalisee("cible")
        if path:
            self.print_log(f"[CAPTURE] Image cible capturée: {path}")
            self.cible.setText(path)

    def capturer_image_contexte(self):
        path = capture_zone_personnalisee("contexte")
        if path:
            self.print_log(f"[CAPTURE] Image contexte capturée: {path}")
            self.contexte.setText(path)

    def charger_actions(self):
        if os.path.exists("actions.json"):
            with open("actions.json", "r") as f:
                self.actions = json.load(f)
        if self.actions: self.print_log(f"[STATE] Chargement des actions: {self.actions[0]}")

    def sauvegarder_actions(self):
        with open("actions.json", "w") as f:
            json.dump(self.actions, f, indent=2)
        self.print_log("[STATE] Actions sauvegardées dans actions.json")

    def toggle_execution(self):
        if not self.execution_en_cours:
            self.start_execution()
        else:
            self.stop_execution_process()

    def start_execution(self):
        if self.execution_en_cours:
            self.print_log("[INFO] Exécution déjà en cours.")
            return

        self.print_log("[INFO] Lancement de l'exécution.")
        self.execution_en_cours = True
        self.stop_execution = False

        nbr = self.spinbox.value()

        def stop_flag():
            return self.stop_execution

        def run():
            def progress_callback(value):
                self.progressValue = value
                self.print_log(f"Progression reçue : {value}")
            try:
                boucle_automatisation(
                    stop_flag=stop_flag,
                    nbr=self.spinbox.value(),
                    on_progress=progress_callback)
            except Exception as e:
                self.print_log(f"[ERREUR] Pendant exécution: {e}")
            finally:
                self.print_log("[INFO] Fin de l'exécution.")
                self.execution_en_cours = False
                self.stop_execution = False

        self.execution_thread = threading.Thread(target=run)
        self.execution_thread.start()

    def stop_execution_process(self):
        if self.execution_en_cours:
            self.print_log("[INFO] Arrêt de l'exécution demandé.")
            self.stop_execution = True
            # Le thread va se terminer naturellement via stop_flag()
        else:
            self.print_log("[INFO] Aucun processus à stopper.")

class FloatingWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        # Frameless et transparent
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.border_visible = True
        self.pen = QPen(Qt.red)
        self.initUI()

        # Lancer le clignotement de la bordure
        self.timer = QTimer()
        self.timer.timeout.connect(self.toggle_border)
        self.timer.start(500)

        # Mettre la fenêtre à la taille de l'écran
        QTimer.singleShot(10, self.set_fullscreen)

    def set_fullscreen(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        self.setGeometry(screen_geometry)

    def initUI(self):

        # ---------- Barre de progression ----------
        self.progress = QProgressBar()
        self.progress.setValue(76)
        self.progress.setTextVisible(True)
        self.progress.setFixedWidth(220)
        self.progress.setFormat("Progress %p%")
        self.progress.setFixedHeight(50)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #C91515;
                border-radius: 8px;
                background-color: #1e1e1e;
                font-weight: 500;
                font-size: 18px;
                font-family: Inter;
                text-align: center;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #C91515;
                border-radius: 0;
            }
        """)

        # ---------- Bouton de fermeture ----------
        self.btn = QPushButton()
        self.btn.setIcon(QIcon("icons/close.svg"))  # remplace par une icône valide si besoin
        self.btn.setIconSize(QSize(40, 40))
        self.btn.setFixedSize(60, 60)
        self.btn.setStyleSheet("""
            QPushButton {
                background-color: #C91515;
                border-radius: 8px;
            }
        """)
        self.btn.clicked.connect(self.close_and_return)

        # ---------- Layout intérieur ----------
        box_layout = QVBoxLayout()
        box_layout.addStretch()
        box_layout.addWidget(self.progress)
        box_layout.addWidget(self.btn, alignment=Qt.AlignRight)

        # ---------- Layout principal (centré bas droite) ----------
        wrapper_layout = QHBoxLayout(self)
        wrapper_layout.setContentsMargins(0, 0, 20, 20)
        wrapper_layout.addStretch()
        inner_layout = QVBoxLayout()
        inner_layout.addStretch()
        inner_layout.addLayout(box_layout)
        wrapper_layout.addLayout(inner_layout)

    def toggle_border(self):
        self.border_visible = not self.border_visible
        self.progress.setValue(int(self.main_window.progressValue))
        self.update()
        if int(self.main_window.progressValue) == 100:
            self.progress.setStyleSheet("""
                QProgressBar {
                    border: 2px solid green;
                    border-radius: 8px;
                    background-color: #1e1e1e;
                    font-weight: 500;
                    font-size: 18px;
                    font-family: Inter;
                    text-align: center;
                    color: white;
                }
                QProgressBar::chunk {
                    background-color: green;
                    border-radius: 0;
                }
            """)
            self.btn.setStyleSheet("""
                QPushButton {
                    background-color: green;
                    border-radius: 8px;
                }
            """)
            self.pen.setColor(Qt.green)

    def paintEvent(self, event):
        if self.border_visible:
            painter = QPainter(self)
            self.pen.setWidth(2)
            self.pen.setStyle(Qt.DashLine)
            painter.setPen(self.pen)
            painter.drawRect(self.rect().adjusted(1, 1, -2, -2))
                 
    def close_and_return(self):
        self.main_window.stop_execution = True  # Stop l'exécution si en cours
        self.main_window.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    main_window = MyApp()
    floating_window = FloatingWindow(main_window)

    # Lancer la fenêtre flottante quand on clique sur START
    main_window.start_btn.clicked.connect(lambda: (
        floating_window.show(),
        main_window.hide()
    ))

    main_window.show()
    sys.exit(app.exec_())

    