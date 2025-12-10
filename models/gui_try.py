import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from datetime import datetime, timedelta
from PyQt5.QtCore import Qt
from settings import Settings 

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
        TODO: Implementovat po přidání dat k dnům
        """
        pass
    
    def __init__(self):
        """
        Inicializace hlavního okna - nastavení GUI, načtení settings, zobrazení týdne
        """
        super().__init__()
        
        # ===== NAČTENÍ SETTINGS =====
        self.settings = Settings()
        
        # První přihlášení? Ulož dnešní datum jako start
        if self.settings.is_first_login():
            self.settings.set_start_date(datetime.now())
            # TODO: Popup okno pro nastavení goals
        
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
        start_weekday = self.settings.get_start_weekday()
        days = self.get_rotated_days(start_weekday)
        
        # Získej datumy pro aktuální týden
        week_dates = self.get_week_dates(self.current_week)
        
        # Vytvoř sloupec pro každý den
        for i, day in enumerate(days):
            # Vertikální layout pro jeden den (věci pod sebou)
            day_column = QVBoxLayout()
            
            # Formátuj datum (9.12)
            date = week_dates[i]
            date_str = f"{date.day}.{date.month}"
            
            # Label s názvem dne a datem
            day_label = QLabel(f"{day}\n{date_str}")
            day_label.setAlignment(Qt.AlignCenter)
            day_label.setStyleSheet("color: white; font-size: 18px;")
            day_column.addWidget(day_label)
            
            # Prostor pro tasky (zatím prázdný, později zde budou úkoly)
            day_column.addStretch()
            
            # Přidej sloupec dne do kontejneru
            days_container.addLayout(day_column)
            
            # Přidej vertikální čáru mezi dny (kromě posledního)
            if i < len(days) - 1:
                separator = QFrame()
                separator.setFrameShape(QFrame.VLine)  # Vertikální linka
                separator.setStyleSheet("color: white;")
                days_container.addWidget(separator)

        # Přidej kontejner dnů do main_layout
        main_layout.addLayout(days_container)

        # ===== FINALIZACE =====
        central_widget.setLayout(main_layout)

        # Na Week 1 je Previous vypnutý (nemůžeme jít zpět)
        if self.current_week <= 1:
            self.previous_button.setEnabled(False)

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
        
        # TODO: Aktualizuj data dnů
        # self.update_week_display()

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
        
        # TODO: Aktualizuj data dnů
        # self.update_week_display()

# ===== SPUŠTĚNÍ APLIKACE =====
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeekView()
    window.show()
    sys.exit(app.exec_())
