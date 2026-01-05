"""
12 Week Planner - Main Entry Point

Spouštěcí soubor aplikace
"""

import sys
from PyQt5.QtWidgets import QApplication
from gui import WeekView


def main():
    """
    Hlavní funkce - spustí aplikaci
    """
    # Vytvoř aplikaci
    app = QApplication(sys.argv)
    
    # Vytvoř hlavní okno
    window = WeekView()
    
    # Zobraz okno
    window.show()
    
    # Spusť event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
 