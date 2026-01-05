from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLabel, 
                             QLineEdit, QTextEdit, QHBoxLayout, QPushButton)


# ===== DIALOG PRO PŘIDÁNÍ NOTE =====
class AddNoteDialog(QDialog):
    """
    Popup dialog pro přidání nové poznámky
    """
    def __init__(self, date, parent=None):
        super().__init__(parent)
        self.date = date
        self.note_data = None  # Sem uložíme data když user klikne Save
        
        # Nastavení okna
        self.setWindowTitle("Add Note")
        self.setModal(True)
        self.setFixedSize(500, 400)
        
        # Layout
        layout = QVBoxLayout()
        
        # Formulář
        form_layout = QFormLayout()
        
        # Datum (read-only)
        date_label = QLabel(date.strftime("%d.%m.%Y"))
        date_label.setStyleSheet("color: gray;")
        form_layout.addRow("Date:", date_label)
        
        # Subclass
        self.subclass_input = QLineEdit()
        self.subclass_input.setPlaceholderText("e.g. math, programming, health")
        form_layout.addRow("Subclass:", self.subclass_input)
        
        # Topic
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("What is this note about?")
        form_layout.addRow("Topic:", self.topic_input)
        
        layout.addLayout(form_layout)
        
        # Text (větší textové pole)
        text_label = QLabel("Note Text:")
        layout.addWidget(text_label)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Write your note here...")
        self.text_input.setMinimumHeight(150)
        layout.addWidget(self.text_input)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_note)
        save_button.setStyleSheet("background-color: white; color: black;")
        
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(save_button)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def save_note(self):
        """
        Uloží note data a zavře dialog
        """
        # Získej hodnoty
        subclass = self.subclass_input.text().strip()
        topic = self.topic_input.text().strip()
        text = self.text_input.toPlainText().strip()
        
        # Validace
        if not topic:
            print("ERROR: Topic is required!")
            return
        
        if not text:
            print("ERROR: Note text is required!")
            return
        
        # Ulož data (v formátu pro note.create_note)
        # [date_value, subclass, topic, text]
        self.note_data = [
            self.date,
            subclass if subclass else "general",
            topic,
            text
        ]
        
        # Zavři dialog
        self.accept()