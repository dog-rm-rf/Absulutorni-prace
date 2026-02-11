"""
Cycles History Dialog - zobrazení všech 12týdenních cyklů
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox)
from PyQt5.QtCore import Qt
from datetime import datetime


class CyclesHistoryDialog(QDialog):
    """
    Dialog zobrazující historii všech cyklů
    """
    
    def __init__(self, cycles_manager, parent=None):
        super().__init__(parent)
        self.cycles_manager = cycles_manager
        
        self.setWindowTitle("Cycles History")
        self.setModal(True)
        self.setFixedSize(700, 500)
        
        self.setup_ui()
        self.load_cycles()
    
    def setup_ui(self):
        """
        Vytvoří UI layoutu
        """
        layout = QVBoxLayout()
        
        # Nadpis
        title = QLabel("📊 Cycles History")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        # Tabulka cyklů
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Cycle #", 
            "Start Date", 
            "End Date", 
            "Status", 
            "Duration"
        ])
        
        # Styling tabulky
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #2D2D2D;
                color: white;
                border: 1px solid #3D3D3D;
                gridline-color: #3D3D3D;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #3D3D3D;
            }
            QHeaderView::section {
                background-color: #1E1E1E;
                color: white;
                padding: 8px;
                border: 1px solid #3D3D3D;
                font-weight: bold;
            }
        """)
        
        # Roztáhni sloupce
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Cycle #
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Start
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # End
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Status
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Duration
        
        layout.addWidget(self.table)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #3D3D3D;
                color: white;
                padding: 10px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
        """)
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
        
        self.setLayout(layout)
        
        # Styling dialogu
        self.setStyleSheet("""
            QDialog {
                background-color: #1E1E1E;
            }
        """)
    
    def load_cycles(self):
        """
        Načte všechny cykly do tabulky
        """
        cycles = self.cycles_manager.get_all_cycles_summary()
        
        if not cycles:
            # Žádné cykly
            self.table.setRowCount(1)
            item = QTableWidgetItem("No cycles found")
            item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(0, 0, item)
            self.table.setSpan(0, 0, 1, 5)  # Merge všechny sloupce
            return
        
        # Seřaď podle ID (nejnovější první)
        cycles_sorted = sorted(cycles, key=lambda c: c['id'], reverse=True)
        
        self.table.setRowCount(len(cycles_sorted))
        
        for row, cycle in enumerate(cycles_sorted):
            # Cycle #
            cycle_id = QTableWidgetItem(f"#{cycle['id']}")
            cycle_id.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 0, cycle_id)
            
            # Start Date
            start_date = cycle['start_date'].strftime("%d.%m.%Y")
            start_item = QTableWidgetItem(start_date)
            start_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 1, start_item)
            
            # End Date
            end_date = cycle['end_date'].strftime("%d.%m.%Y")
            end_item = QTableWidgetItem(end_date)
            end_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 2, end_item)
            
            # Status
            status = cycle['status']
            if status == "active":
                status_text = "✅ Active"
                color = "#00FF00"
            else:
                status_text = "📦 Archived"
                color = "#888888"
            
            status_item = QTableWidgetItem(status_text)
            status_item.setTextAlignment(Qt.AlignCenter)
            status_item.setForeground(Qt.white)
            self.table.setItem(row, 3, status_item)
            
            # Duration (kolik dní)
            duration_days = (cycle['end_date'] - cycle['start_date']).days
            duration_item = QTableWidgetItem(f"{duration_days} days")
            duration_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 4, duration_item)