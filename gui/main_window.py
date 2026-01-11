from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QFrame, QScrollArea, QDialog)
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime, timedelta

# Import našich vlastních tříd
from .day_widget import DayWidget
from .add_task_dialog import AddTaskDialog
from .add_note_dialog import AddNoteDialog
from .add_reward_dialog import AddRewardDialog
from .set_goals_dialog import SetGoalsDialog 

# Import backendu
from models.settings import Settings
from models.all_tasks import All_tasks
from models.goal import Goal
from models.notes_class import Note
from models.reward import Reward


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
        
        
        # DEBUG
        print(f"DEBUG: Načtený start_date: {self.settings.start_date}")
        print(f"DEBUG: is_first_login(): {self.settings.is_first_login()}")
        print(f"DEBUG: needs_new_cycle(): {self.settings.needs_new_cycle()}")

        # Načti backend objekty
        self.all_tasks = All_tasks()
        self.goal = Goal(self.all_tasks)
        self.note = Note() 
        self.reward = Reward()

        #debug tasks
        #print(f"DEBUG: Celkem tasků: {len(self.all_tasks.list_of_all_tasks_objects)}")

        for task in self.all_tasks.list_of_all_tasks_objects:
            print(f"DEBUG: Task: {task[0]}, Date: {task[2]}")

        # DUMMY DATA - smaž později
        dummy_task = ["Test Task", "test", datetime.now(), 2, None, []]
        self.all_tasks.list_of_all_tasks_objects.append(dummy_task)
        print(f"DEBUG: Přidal jsem dummy task s datem: {datetime.now().date()}")
        
        # DEBUG: Zobraz načtené hodnoty
        print(f"DEBUG: is_first_login = {self.settings.is_first_login()}")
        print(f"DEBUG: start_date = {self.settings.start_date}")
        
        # První přihlášení? Nastav start_date
        if self.settings.is_first_login():
            print("DEBUG: Nastavuji start_date na dnes")
            self.settings.set_start_date(datetime.now())
            self.show_goals_dialog()  # ← Zobraz goals popup
            
        # Nebo uplynulo 12 týdnů? Nový cyklus = nové goals
        elif self.settings.needs_new_cycle():
            # Reset start_date na dnes
            self.settings.set_start_date(datetime.now())
            self.show_goals_dialog()  # ← Zobraz goals popup
            
            # Smaž staré goals (začínáme nový cyklus)
            self.goal.list_of_all_goals_objects = []
            self.goal.update_data_frame()
            
        
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
        
        # Manage button (vpravo)
        manage_button = QPushButton("Manage")
        manage_button.setStyleSheet("background-color: #FF9800; color: white; font-size: 16px;")
        manage_button.clicked.connect(self.open_management_dialog)
        top_layout.addWidget(manage_button)

        # Přidej horní lištu do main_layout
        main_layout.addLayout(top_layout)

        # ===== DNY V TÝDNU (Mon-Sun s datumy) =====
        
        # Kontejner pro dny (horizontální - vedle sebe)
        days_container = QHBoxLayout()

        # Zjisti který den byl start a rotuj dny
        start_weekday = self.settings.get_start_weekday()
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
        
        # ===== ZKONTROLUJ GOALS =====
        print(f"DEBUG: has_active_goals() = {self.has_active_goals()}")
        print(f"DEBUG: počet goals = {len(self.goal.list_of_all_goals_objects)}")
        if not self.has_active_goals():
            # Zobraz popup až po 100ms (až se okno zobrazí)
            print("DEBUG: Volám show_goals_dialog()")
            QTimer.singleShot(100, self.show_goals_dialog)
        else:
            print("DEBUG: Goals už existují, popup se nezobrazí")
            print(self.goal.list_of_all_goals_objects)
            
    def open_management_dialog(self):
        """
        Otevře management dialog
        """
        from .management_dialog import ManagementDialog
        
        dialog = ManagementDialog(self, self.all_tasks, self.goal, self.note, self.reward)
        dialog.exec_()
        
        # Refresh GUI po zavření dialogu
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
            
    def show_goals_dialog(self):
        """
        Zobrazí dialog pro nastavení goals
        """
        dialog = SetGoalsDialog(self)
        result = dialog.exec_()
        
        if result == QDialog.Accepted:
            goals = dialog.goals_data
            
            # Vypočítej start a end date pro tento cyklus
            cycle_start = self.settings.start_date
            cycle_end = cycle_start + timedelta(days=84)  # 12 týdnů = 84 dní
            
            # Ulož každý goal do backendu
            for goal_list in goals:
                goal_data = [
                    goal_list[0],   # 0 - goal_name
                    goal_list[1],   # 1 - subclass
                    goal_list[2],   # 2 - timer
                    goal_list[3],   # 3 - average_score
                    cycle_start,    # 4 - date_of_creation
                    False,          # 5 - checked
                    cycle_end,      # 6 - end_date
                    False           # 7 - completed
                ]
                self.goal.add_goal(goal_data)
                print(f"✅ Goal: {goal_list[0]} | {goal_list[2]}h | score {goal_list[3]}")
            
            # Označ že goals byly nastaveny
            self.settings.set_goals_completed(True)
            
            # Zobraz potvrzení
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(
                self,
                "Goals Set!",
                f"You've set {len(goals)} goals for the next 12 weeks.\n\n"
                "Stay focused and achieve them! 💪"
            )
            
    def has_active_goals(self):
        """
        Zkontroluje jestli má uživatel nastavené goals pro aktuální cyklus
        
        Returns:
            bool: True pokud má goals, False pokud nemá
        """
        
        if not self.goal.list_of_all_goals_objects:
            return False
        
        # Zkontroluj jestli má alespoň 1 goal
        if len(self.goal.list_of_all_goals_objects) < 1:
            return False
        
        return True
    
    def get_current_cycle_goals(self):
        """
        Vrátí goals pro aktuální cyklus
        """
        current_start = self.settings.start_date
        
        # Filtruj goals podle start_date
        current_goals = []
        for goal in self.goal.list_of_all_goals_objects:
            # Starý formát - přeskoč
            if len(goal) < 8:
                # Rozšířený formát: date_of_creation je na indexu 4
                goal_start_date = goal[4]
                
                # Porovnej start_date (jen datum, ne čas)
                if isinstance(goal_start_date, datetime):
                    goal_start_date = goal_start_date.date()
                
                if isinstance(current_start, datetime):
                    current_start_date = current_start.date()
                else:
                    current_start_date = current_start
                
                # Je tento goal z aktuálního cyklu?
                if goal_start_date == current_start_date:
                    current_goals.append(goal)
        
        return current_goals