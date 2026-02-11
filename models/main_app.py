import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QMenu, QDialog, QLineEdit, QSpinBox, QFormLayout, QTextEdit, QScrollArea
from datetime import datetime, timedelta
from PyQt5.QtCore import Qt
from settings import Settings 
from all_tasks import All_tasks  
from goal import Goal 
from notes_class import Note
from reward import Reward 

# ===== DIALOG PRO PŘIDÁNÍ TASKU =====
class AddTaskDialog(QDialog):
    """
    Popup dialog pro přidání nového tasku
    """
    def __init__(self, date, parent=None):
        super().__init__(parent)
        self.date = date
        self.task_data = None  # Sem uložíme data když user klikne Save
        
        # Nastavení okna
        self.setWindowTitle("Add Task")
        self.setModal(True)  # Blokuje hlavní okno dokud se nezavře
        self.setFixedSize(400, 250)
        
        # Layout
        layout = QVBoxLayout()
        
        # Formulář
        form_layout = QFormLayout()
        
        # Datum (read-only, jen zobrazení)
        date_label = QLabel(date.strftime("%d.%m.%Y"))
        date_label.setStyleSheet("color: gray;")
        form_layout.addRow("Date:", date_label)
        
        # Task Name
        self.task_name_input = QLineEdit()
        self.task_name_input.setPlaceholderText("Enter task name")
        form_layout.addRow("Task Name:", self.task_name_input)
        
        # Subclass
        self.subclass_input = QLineEdit()
        self.subclass_input.setPlaceholderText("e.g. programming, health")
        form_layout.addRow("Subclass:", self.subclass_input)
        
        # Hours a Minutes - vytvoř horizontal layout
        time_layout = QHBoxLayout()
        
        # Hours SpinBox
        self.hours_input = QSpinBox()
        self.hours_input.setMinimum(0)
        self.hours_input.setMaximum(24)
        self.hours_input.setValue(2)  # Default 2 hodiny
        self.hours_input.setSuffix(" h")  # Přidá "h" za číslo
        
        # Minutes SpinBox
        self.minutes_input = QSpinBox()
        self.minutes_input.setMinimum(0)
        self.minutes_input.setMaximum(59)
        self.minutes_input.setSingleStep(15)  # Krok po 15 minutách
        self.minutes_input.setValue(0)  # Default 0 minut
        self.minutes_input.setSuffix(" min")  # Přidá "min" za číslo
        
        # Přidej oba do horizontal layoutu
        time_layout.addWidget(self.hours_input)
        time_layout.addWidget(self.minutes_input)
        
        # Přidej celý time_layout do formuláře
        form_layout.addRow("Time:", time_layout)
        
        layout.addLayout(form_layout)
        
        # Buttons (Cancel, Save)
        buttons_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)  # Zavře dialog bez uložení
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_task)
        save_button.setStyleSheet("background-color: #FFFFFF; color: black;")
        
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(save_button)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def save_task(self):
        """
        Uloží data a zavře dialog
        """
        # Získej hodnoty z inputů
        task_name = self.task_name_input.text().strip()
        subclass = self.subclass_input.text().strip()
        # Získej hodiny a minuty
        hours = self.hours_input.value()
        minutes = self.minutes_input.value()
        
        # Převeď na desetinné číslo (např. 2h 30min = 2.5)
        total_hours = hours + (minutes / 60.0)
        
        # Validace
        if not task_name:
            # TODO: Zobrazit chybovou hlášku
            print("ERROR: Task name is required!")
            return
        
        # Ulož data (v formátu pro all_tasks.add_new_task)
        # [task_name, task_sub_class, task_date, desired_time_spent, score, review]
        self.task_data = [
            task_name,
            subclass if subclass else "general",  # Default subclass
            self.date,
            total_hours,
            None,  # score (zatím None)
            ["", "", ""]  # review (learnt, dont_understand, next_step)
        ]
        
        # Zavři dialog s úspěchem
        self.accept()

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
        
# ===== DIALOG PRO PŘIDÁNÍ REWARD =====
class AddRewardDialog(QDialog):
    """
    Popup dialog pro přidání odměny
    """
    def __init__(self, date, parent=None):
        super().__init__(parent)
        self.date = date
        self.reward_data = None
        
        # Nastavení okna
        self.setWindowTitle("Add Reward")
        self.setModal(True)
        self.setFixedSize(400, 250)
        
        # Layout
        layout = QVBoxLayout()
        
        # Formulář
        form_layout = QFormLayout()
        
        # Datum (read-only)
        date_label = QLabel(date.strftime("%d.%m.%Y"))
        date_label.setStyleSheet("color: gray;")
        form_layout.addRow("Date:", date_label)
        
        # Reward Name
        self.reward_name_input = QLineEdit()
        self.reward_name_input.setPlaceholderText("e.g. Watch movie, Play games")
        form_layout.addRow("Reward:", self.reward_name_input)
        
        # Time - Hours and Minutes
        time_layout = QHBoxLayout()
        
        self.hours_input = QSpinBox()
        self.hours_input.setMinimum(0)
        self.hours_input.setMaximum(24)
        self.hours_input.setValue(1)
        self.hours_input.setSuffix(" h")
        
        self.minutes_input = QSpinBox()
        self.minutes_input.setMinimum(0)
        self.minutes_input.setMaximum(59)
        self.minutes_input.setSingleStep(15)
        self.minutes_input.setValue(0)
        self.minutes_input.setSuffix(" min")
        
        time_layout.addWidget(self.hours_input)
        time_layout.addWidget(self.minutes_input)
        
        form_layout.addRow("Time:", time_layout)
        
        layout.addLayout(form_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_reward)
        save_button.setStyleSheet("background-color: white; color: black;")
        
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(save_button)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def save_reward(self):
        """
        Uloží reward data
        """
        # Získej hodnoty
        reward_name = self.reward_name_input.text().strip()
        hours = self.hours_input.value()
        minutes = self.minutes_input.value()
        
        # Validace
        if not reward_name:
            print("ERROR: Reward name is required!")
            return
        
        # Převeď na desetinné číslo
        total_hours = hours + (minutes / 60.0)
        
        # Ulož data (v formátu pro reward.add_reward)
        # [date_of_creation, reward_name, time, finished]
        self.reward_data = [
            self.date,
            reward_name,
            total_hours,
            False  # finished = False (ještě nesplněno)
        ]
        
        # Zavři dialog
        self.accept()

# ===== TŘÍDA PRO JEDEN DEN =====
class DayWidget(QWidget):
    """
    Widget pro jeden den - umožňuje context menu (pravé tlačítko)
    """
    #widget je top-level (např. samostatné okno) a musí být spravován ručně reference na parent=None
    def __init__(self, date, parent=None, note_obj=None, reward_obj=None): #tohle jsou parametry, potrebujeme date, a parent je volitelny
        super().__init__(parent) # kdyz neuvedeme parent tak parent je QWidget
        self.date = date  # Uložíme si datum tohoto dne
        self.parent_window = parent  # Odkaz na hlavní okno
        self.note_obj = note_obj
        self.reward_obj = reward_obj 
        
        # Nastav maximální šířku sloupce
        self.setMaximumWidth(200)

        # Layout pro tento den
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Povolit context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_note_detail(self, note):
        """
        Zobrazí detail note v popup okně
        """
        # note = [date, subclass, topic, text]
        date = note[0]
        subclass = note[1]
        topic = note[2]
        text = note[3]
        
        # Vytvoř popup dialog
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Note: {topic}")
        dialog.setModal(True)
        dialog.setMinimumSize(500, 400)
        
        # Layout
        layout = QVBoxLayout()
        
        # Info (datum, subclass)
        info_label = QLabel(f"📅 {date.strftime('%d.%m.%Y')} | 🏷️ {subclass}")
        info_label.setStyleSheet("color: gray; font-size: 12px;")
        layout.addWidget(info_label)
        
        # Topic (nadpis)
        topic_label = QLabel(topic)
        topic_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        layout.addWidget(topic_label)
        
        # Text (obsah)
        text_display = QTextEdit()
        text_display.setPlainText(text)
        text_display.setReadOnly(True)  # Jen čtení, ne editace
        layout.addWidget(text_display)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(dialog.close)
        layout.addWidget(close_button)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def show_context_menu(self, position):
        """
        Zobrazí context menu při pravém kliknutí
        """
        # Vytvoř menu
        menu = QMenu(self)
        
        # Přidej akce (možnosti)
        add_task_action = menu.addAction("Add Task")
        add_note_action = menu.addAction("Add Note")    
        add_reward_action = menu.addAction("Add Reward")
        
        # Zobraz menu a čekej na kliknutí
        action = menu.exec_(self.mapToGlobal(position))
        
        # Zjisti co uživatel klikl
        if action == add_task_action:
            self.parent_window.add_task_for_date(self.date)
        elif action == add_note_action:
            self.parent_window.add_note_for_date(self.date)
        elif action == add_reward_action:
            self.parent_window.add_reward_for_date(self.date)


    def update_content(self, date, day_name, all_tasks_obj, note_obj=None, reward_obj=None):
        """
        Aktualizuje obsah widgetu (datum + tasky) pro nový týden
        
        Args:
            date: Nové datum pro tento widget
            day_name: Název dne (Mon, Tue, ...)
            all_tasks_obj: Odkaz na All_tasks objekt
        """
        self.note_obj = note_obj 
        self.reward_obj = reward_obj
        # Zakaž překreslování během aktualizace
        self.setUpdatesEnabled(False)

        # Aktualizuj uložené datum
        self.date = date
        
        # Vyčisti layout (smaž všechny widgety)
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Formátuj datum
        date_str = f"{date.day}.{date.month}"
        
        # Vytvoř nový day_label
        day_label = QLabel(f"{day_name}\n{date_str}")
        day_label.setAlignment(Qt.AlignCenter)
        day_label.setStyleSheet("color: white; font-size: 18px;")
        self.layout.addWidget(day_label)
        
        # Získej tasky pro tento den
        tasks_for_day = self.get_tasks_for_date(date, all_tasks_obj)
        
        # Vytvoř label pro každý task
        for task in tasks_for_day:
            task_name = task[0]
            task_hours = task[3]
            
            # Zkrať název pokud je moc dlouhý
            max_length = 18    
            display_name = task_name if len(task_name) <= max_length else task_name[:max_length] + "..."
            
            task_label = QLabel(f"• {display_name}\n ({task_hours}h)")
            task_label.setAlignment(Qt.AlignLeft)
            task_label.setStyleSheet("color: lightgray; font-size: 14px; padding-left: 10px;")
            task_label.setToolTip(task_name)
            self.layout.addWidget(task_label)
        
        # ===== ZOBRAZENÍ NOTES PRO TENTO DEN =====
        if self.note_obj:  # Kontrola jestli máme note_obj
            notes_for_day = self.get_notes_for_date(date, self.note_obj)
            
            # Vytvoř label pro každou note
            for note in notes_for_day:
                note_topic = note[2]  # topic je na indexu 2
                
                # Zkrať topic pokud je moc dlouhý
                max_length = 18
                display_topic = note_topic if len(note_topic) <= max_length else note_topic[:max_length] + "..."
                
                # Note label (jiná barva - žlutá/oranžová)
                note_label = QLabel(f"📝 {display_topic}")
                note_label.setAlignment(Qt.AlignLeft)
                note_label.setStyleSheet("color: #FFA500; font-size: 14px; padding-left: 10px;")
                note_label.setToolTip(note_topic)
                
                # Ulož si note data do labelu (abychom je mohli zobrazit při kliknutí)
                note_label.setProperty("note_data", note)
                
                # Povolit kliknutí na label
                note_label.setCursor(Qt.PointingHandCursor)  # Kurzor se změní na ruku
                note_label.mousePressEvent = lambda event, n=note: self.show_note_detail(n)
                
                self.layout.addWidget(note_label)
            
        # ===== ZOBRAZENÍ REWARDS PRO TENTO DEN =====
        if self.reward_obj:
            rewards_for_day = self.get_rewards_for_date(date, self.reward_obj)
        
            # Vytvoř label pro každou reward
            for reward in rewards_for_day:
                reward_name = reward[1]  # reward_name je na indexu 1
                reward_time = reward[2]  # time
                reward_finished = reward[3]  # finished
                
                # Ikona podle toho jestli je splněno
                icon = "✅" if reward_finished else "🎁"
                
                # Zkrať název pokud je moc dlouhý
                max_length = 18  # O trochu kratší kvůli ikoně
                display_reward = reward_name if len(reward_name) <= max_length else reward_name[:max_length] + "..."
                
                # Reward label (zelená barva)
                reward_label = QLabel(f"{icon} {display_reward}\n ({reward_time}h)")
                reward_label.setAlignment(Qt.AlignLeft)
                reward_label.setStyleSheet("color: #00FF00; font-size: 14px; padding-left: 10px;")
                reward_label.setToolTip(reward_name)
                
                self.layout.addWidget(reward_label)
        
        # Prostor pod tasky a notes
        self.layout.addStretch()

        # Povol překreslování a aktualizuj
        self.setUpdatesEnabled(True)
        self.update()

        
    def get_tasks_for_date(self, date, all_tasks_obj):
        """
        Vrátí tasky pro dané datum
        """
        tasks_for_day = []
        
        for task in all_tasks_obj.list_of_all_tasks_objects:
            task_date = task[2]
            
            if isinstance(task_date, datetime):
                task_date = task_date.date()
            
            if task_date == date.date():
                tasks_for_day.append(task)
        
        return tasks_for_day
    
    def get_notes_for_date(self, date, note_obj):
        """
        Vrátí notes pro dané datum
        """
        notes_for_day = []
        
        for note in note_obj.list_of_all_notes_objects:
            # note[0] = date (první prvek)
            note_date = note[0]
            
            if isinstance(note_date, datetime):
                note_date = note_date.date()
            
            if note_date == date.date():
                notes_for_day.append(note)
        
        return notes_for_day
    
    def get_rewards_for_date(self, date, reward_obj):
        """
        Vrátí rewards pro dané datum
        """
        rewards_for_day = []
        
        for reward in reward_obj.list_of_all_reward_objects:
            # reward[0] = date_of_creation
            reward_date = reward[0]
            
            if isinstance(reward_date, datetime):
                reward_date = reward_date.date()
            
            if reward_date == date.date():
                rewards_for_day.append(reward)
        
        return rewards_for_day
    
# ===== HLAVNÍ OKNO =====
class WeekView(QMainWindow):
    """
    Hlavní okno aplikace - zobrazuje týdenní kalendář (7 dní)
    S navigací Previous/Next pro přepínání mezi týdny (1-12)
    """

    def get_rotated_days(self, start_weekday):
        """
        Rotuje názvy dnů podle toho, kterým dnem začal uživatel
        
        Args:
            start_weekday (int): Den v týdnu kdy začal (0=Mon, 1=Tue, ..., 6=Sun)
            
        Returns:
            list: Rotovaný list dnů (např. ["Wed", "Thu", "Fri", "Sat", "Sun", "Mon", "Tue"])
        
        Příklad:
            Pokud uživatel začal ve středu (2):
            ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            → ["Wed", "Thu", "Fri", "Sat", "Sun", "Mon", "Tue"]
        """
        all_days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        return all_days[start_weekday:] + all_days[:start_weekday]
    
    def get_week_dates(self, week_number):
        """
        Vypočítá konkrétní data (datetime objekty) pro daný týden
        
        Args:
            week_number (int): Číslo týdne (1-12)
            
        Returns:
            list: List 7 datetime objektů (pondělí až neděle toho týdne)
        
        Příklad:
            Week 1, start_date = středa 11.12.2024
            → vrátí [středa 11.12, čtvrtek 12.12, ..., úterý 17.12]
        """
        # Kolik dní od start_date je začátek tohoto týdne?
        days_offset = (week_number - 1) * 7
        
        # První den tohoto týdne
        week_start = self.settings.start_date + timedelta(days=days_offset)
        
        # Vytvoř list 7 po sobě jdoucích dat
        dates = []
        for i in range(7):
            date = week_start + timedelta(days=i)
            dates.append(date)
        
        return dates
    
    
        
    def update_week_display(self):
        """
        Aktualizuje zobrazení dnů a dat po změně týdne (Next/Previous)
        """
        # Získej nová data pro aktuální týden
        week_dates = self.get_week_dates(self.current_week)
    
         # Aktualizuj každý DayWidget (datum + tasky)
        for i, day_widget in enumerate(self.day_widgets):
            date = week_dates[i]
            day_name = self.days[i]
        
            # Aktualizuj obsah widgetu
            day_widget.update_content(date, day_name, self.all_tasks, self.note, self.reward)
    
    def __init__(self):
        """
        Inicializace hlavního okna - nastavení GUI, načtení settings, zobrazení týdne
        """
        super().__init__()
        
        # ===== NAČTENÍ SETTINGS =====
        self.settings = Settings()

        # Načti backend objekty
        self.all_tasks = All_tasks()
        self.goal = Goal(self.all_tasks)
        self.note = Note() 
        self.reward = Reward()
        
        # Spočítej na kterém týdnu jsme (1-12)
        self.current_week = self.settings.calculate_current_week()
        
        # ===== NASTAVENÍ HLAVNÍHO OKNA =====
        self.setWindowTitle("12 Week Planner")
        self.setGeometry(0, 0, 1920, 1080) 
        self.setStyleSheet("""
            background-color: black;
            color: white;
            font-size: 16px;
        """)
        
        # ===== VYTVOŘENÍ CENTRAL WIDGET A MAIN LAYOUT =====
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()  # Vertikální layout (věci pod sebou)

        # ===== HORNÍ LIŠTA (Previous, Week X, Next) =====
        
        # Previous button (vlevo)
        self.previous_button = QPushButton("Previous")
        self.previous_button.setStyleSheet("background-color: white; color: black; font-size: 16px;")    
        self.previous_button.clicked.connect(self.previous_week)

        # Week label (uprostřed)
        self.week_label = QLabel(f"Week {self.current_week}")
        self.week_label.setAlignment(Qt.AlignCenter)
        self.week_label.setStyleSheet("color: white; font-size: 24px;")

        # Next button (vpravo)
        self.next_button = QPushButton("Next")
        self.next_button.setStyleSheet("background-color: white; color: black; font-size: 16px;")
        self.next_button.clicked.connect(self.next_week)

        # Horizontální layout pro horní lištu (věci vedle sebe)
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.previous_button)
        top_layout.addWidget(self.week_label)
        top_layout.addWidget(self.next_button)

        # Přidej horní lištu do main_layout
        main_layout.addLayout(top_layout)

        # ===== DNY V TÝDNU (Mon-Sun s datumy) =====
        
        # Kontejner pro dny (horizontální - vedle sebe)
        days_container = QHBoxLayout()

        # Zjisti který den byl start a rotuj dny
        active_cycle = self.cycles_manager.get_active_cycle()
        if active_cycle:
            start_weekday = active_cycle['start_date'].weekday()
        else:
            start_weekday = 0  # Monday default

        self.days = self.get_rotated_days(start_weekday)  # Ulož jako self.days
        days = self.days  # Použij v loopu

        
        # Získej datumy pro aktuální týden
        week_dates = self.get_week_dates(self.current_week)

        # List pro uložení day_labels (abychom je mohli aktualizovat)
        self.day_labels = []  

        # List pro uložení day_widgets (abychom mohli aktualizovat tasky)
        self.day_widgets = []  
        
        # Vytvoř sloupec pro každý den
        for i, day in enumerate(days): #do i poradi od 0 a do day den z days
            date = week_dates[i]
            date_str = f"{date.day}.{date.month}"
            
            # Vytvoř widget pro den (místo layoutu)
            day_widget = DayWidget(date, self, self.note, self.reward)


            # Ulož si widget pro pozdější aktualizaci
            self.day_widgets.append(day_widget)
            
            # Label s názvem dne a datem
            day_label = QLabel(f"{day}\n{date_str}")
            day_label.setAlignment(Qt.AlignCenter)
            day_label.setStyleSheet("color: white; font-size: 18px;")
            day_widget.layout.addWidget(day_label)
            
            # Ulož si label pro pozdější aktualizaci
            self.day_labels.append(day_label)
            
            # ===== ZOBRAZENÍ TASKŮ PRO TENTO DEN =====
            tasks_for_day = day_widget.get_tasks_for_date(date, self.all_tasks)  
            
            # Vytvoř label pro každý task
            for task in tasks_for_day:
                task_name = task[0]
                task_hours = task[3]
                
                task_label = QLabel(f"• {task_name} ({task_hours}h)")
                task_label.setAlignment(Qt.AlignLeft)
                task_label.setStyleSheet("color: lightgray; font-size: 14px; padding-left: 10px;")
                day_widget.layout.addWidget(task_label)
            
            # Prostor pod tasky
            day_widget.layout.addStretch()
            
            # Přidej widget do kontejneru
            days_container.addWidget(day_widget)
            
            # Přidej vertikální čáru mezi dny
            if i < len(days) - 1:
                separator = QFrame()
                separator.setFrameShape(QFrame.VLine)
                separator.setStyleSheet("color: white;")
                days_container.addWidget(separator)

            # ===== SCROLL AREA =====
        # Vytvoř widget pro days_container
        days_widget = QWidget()
        days_widget.setLayout(days_container)
        
        # Vytvoř scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(days_widget)
        scroll_area.setWidgetResizable(True)  # Důležité - widget se přizpůsobí
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Jen vertikální scroll
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: black; }")
        
        # Přidej scroll area do main_layout (místo days_container)
        main_layout.addWidget(scroll_area)

        # ===== FINALIZACE =====
        central_widget.setLayout(main_layout)

        # Na Week 1 je Previous vypnutý (nemůžeme jít zpět)
        if self.current_week <= 1:
            self.previous_button.setEnabled(False)

        self.update_week_display()

    def next_week(self):
        """
        Handler pro Next button - přepne na další týden
        """
        # Zvýš číslo týdne
        self.current_week += 1
        
        # Aktualizuj text labelu
        self.week_label.setText(f"Week {self.current_week}")
        
        # Zapni Previous (už nejsme na Week 1)
        self.previous_button.setEnabled(True)
        
        # Na Week 12 vypni Next (nemůžeme jít dál)
        if self.current_week >= 12:
            self.next_button.setEnabled(False)
        
        # Aktualizuj data dnů
        self.update_week_display()

    def previous_week(self):
        """
        Handler pro Previous button - přepne na předchozí týden
        """
        # Sniž číslo týdne
        self.current_week -= 1
        
        # Aktualizuj text labelu
        self.week_label.setText(f"Week {self.current_week}")
        
        # Zapni Next (už nejsme na Week 12)
        self.next_button.setEnabled(True)
        
        # Na Week 1 vypni Previous (nemůžeme jít zpět)
        if self.current_week <= 1:
            self.previous_button.setEnabled(False)
        
        # Aktualizuj data dnů
        self.update_week_display()
    
    def add_task_for_date(self, date):
        """
        Otevře popup pro přidání tasku k danému datu
        """
        # Vytvoř a zobraz dialog
        dialog = AddTaskDialog(date, self)
        
        # Čekej na odpověď (uživatel klikne Save nebo Cancel)
        result = dialog.exec_()
        
        # Pokud user klikl Save (ne Cancel)
        if result == QDialog.Accepted:
            # Získej data z dialogu
            task_data = dialog.task_data
            
            # Ulož task do backendu
            self.all_tasks.add_new_task(task_data)
            
            print(f"✅ Task uložen: {task_data[0]}")
            
            # Refresh GUI - aktualizuj zobrazení aktuálního týdne
            self.update_week_display()


    def add_note_for_date(self, date):
        """
        Otevře popup pro přidání note k danému datu
        """
        # Vytvoř a zobraz dialog
        dialog = AddNoteDialog(date, self)
        
        # Čekej na odpověď
        result = dialog.exec_()
        
        # Pokud user klikl Save
        if result == QDialog.Accepted:
            # Získej data
            note_data = dialog.note_data
            
            # Ulož note do backendu
            self.note.create_note(note_data)
            
            print(f"✅ Note uložena: {note_data[2]}")  # topic

    def add_reward_for_date(self, date):
        """
        Otevře popup pro přidání reward k danému datu
        """
        # Vytvoř a zobraz dialog
        dialog = AddRewardDialog(date, self)
        
        # Čekej na odpověď
        result = dialog.exec_()
        
        # Pokud user klikl Save
        if result == QDialog.Accepted:
            # Získej data
            reward_data = dialog.reward_data
            
            # Ulož reward do backendu
            self.reward.add_reward(reward_data)
            
            print(f"✅ Reward uložena: {reward_data[1]}")
            
            # Refresh GUI
            self.update_week_display()






# ===== SPUŠTĚNÍ APLIKACE =====
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeekView()
    window.show()
    sys.exit(app.exec_())
