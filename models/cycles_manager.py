"""
Správce 12týdenních cyklů
Spravuje active cyklus a archiv dokončených cyklů
"""

import os
import pickle
import shutil
from datetime import datetime, timedelta
from .paths import PROJECT_ROOT


class CyclesManager:
    """
    Spravuje cykly - aktivní a archivované
    """
    
    def __init__(self):
        # Cesty
        self.data_dir = os.path.join(PROJECT_ROOT, "data")
        self.active_dir = os.path.join(self.data_dir, "active")
        self.archive_dir = os.path.join(self.data_dir, "archive")
        self.metadata_file = os.path.join(self.data_dir, "cycles_metadata.pkl")
        
        # Vytvoř složky
        os.makedirs(self.active_dir, exist_ok=True)
        os.makedirs(self.archive_dir, exist_ok=True)
        
        # Načti metadata
        self.cycles = self.load_metadata()
    
    def load_metadata(self):
        """
        Načte metadata všech cyklů
        
        Returns:
            list: List cyklů [{"id": 1, "start": datetime, ...}, ...]
        """
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'rb') as f:
                return pickle.load(f)
        else:
            # Žádná metadata - první spuštění
            return []
    
    def save_metadata(self):
        """
        Uloží metadata všech cyklů
        """
        with open(self.metadata_file, 'wb') as f:
            pickle.dump(self.cycles, f)
    
    def get_active_cycle(self):
        """
        Vrátí metadata aktivního cyklu
        
        Returns:
            dict nebo None: {"id": 2, "start": datetime, "status": "active", ...}
        """
        for cycle in self.cycles:
            if cycle.get("status") == "active":
                return cycle
        return None
    
    def create_new_cycle(self, start_date=None):
        """
        Vytvoří nový aktivní cyklus
        
        Args:
            start_date: Datum startu (default: dnes)
        
        Returns:
            dict: Metadata nového cyklu
        """
        if start_date is None:
            start_date = datetime.now()
        
        # Vypočítej cycle_id (max + 1)
        if self.cycles:
            cycle_id = max(c["id"] for c in self.cycles) + 1
        else:
            cycle_id = 1
        
        # Vytvoř metadata
        end_date = start_date + timedelta(days=84)  # 12 týdnů
        
        new_cycle = {
            "id": cycle_id,
            "start_date": start_date,
            "end_date": end_date,
            "status": "active",
            "created_at": datetime.now(),
            "goals_count": 0,
            "tasks_count": 0,
            "total_hours": 0.0
        }
        
        self.cycles.append(new_cycle)
        self.save_metadata()
        
        print(f"✅ Vytvořen nový cyklus #{cycle_id}: {start_date.date()} - {end_date.date()}")
        
        return new_cycle
    
    def archive_current_cycle(self):
        """
        Archivuje aktivní cyklus do archive/
        
        Proces:
        1. Najdi aktivní cyklus
        2. Zkopíruj data z active/ do archive/cycle_XXX.pkl
        3. Označ cyklus jako "completed"
        4. Smaž data z active/
        """
        active = self.get_active_cycle()
        
        if not active:
            print("⚠️ Žádný aktivní cyklus k archivaci")
            return False
        
        cycle_id = active["id"]
        
        # Název archive souboru
        archive_filename = f"cycle_{cycle_id:03d}.pkl"
        archive_path = os.path.join(self.archive_dir, archive_filename)
        
        # Shromáždi všechna data z active/
        archive_data = {
            "metadata": active,
            "tasks": self._load_active_file("tasks_dataframe.pkl"),
            "goals": self._load_active_file("goals_dataframe.pkl"),
            "notes": self._load_active_file("notes_file.pkl"),
            "rewards": self._load_active_file("reward_dataframe.pkl")
        }
        
        # Ulož do archivu
        with open(archive_path, 'wb') as f:
            pickle.dump(archive_data, f)
        
        # Označ jako completed
        active["status"] = "completed"
        active["archived_at"] = datetime.now()
        active["archive_file"] = archive_filename
        
        self.save_metadata()
        
        # Smaž aktivní data
        self._clear_active_directory()
        
        print(f"✅ Cyklus #{cycle_id} archivován do {archive_filename}")
        
        return True
    
    def _load_active_file(self, filename):
        """
        Načte soubor z active/ (pokud existuje)
        """
        filepath = os.path.join(self.active_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                return pickle.load(f)
        return None
    
    def _clear_active_directory(self):
        """
        Smaže všechny soubory z active/
        """
        for filename in os.listdir(self.active_dir):
            filepath = os.path.join(self.active_dir, filename)
            if os.path.isfile(filepath):
                os.remove(filepath)
        print("✅ Active directory vyčištěno")
    
    def load_archive_cycle(self, cycle_id):
        """
        Načte archivovaný cyklus
        
        Args:
            cycle_id: ID cyklu
        
        Returns:
            dict: {"metadata": {...}, "tasks": [...], ...}
        """
        # Najdi cyklus v metadata
        cycle = next((c for c in self.cycles if c["id"] == cycle_id), None)
        
        if not cycle or cycle["status"] != "completed":
            print(f"⚠️ Cyklus #{cycle_id} není archivován")
            return None
        
        archive_filename = cycle.get("archive_file")
        if not archive_filename:
            print(f"⚠️ Chybí archive_file pro cyklus #{cycle_id}")
            return None
        
        archive_path = os.path.join(self.archive_dir, archive_filename)
        
        if not os.path.exists(archive_path):
            print(f"⚠️ Archive soubor neexistuje: {archive_path}")
            return None
        
        # Načti archiv
        with open(archive_path, 'rb') as f:
            return pickle.load(f)
    
    def get_all_cycles_summary(self):
        """
        Vrátí přehled všech cyklů pro statistiky
        
        Returns:
            list: [{"id": 1, "start": ..., "goals": 5, "tasks": 120}, ...]
        """
        summary = []
        
        for cycle in self.cycles:
            cycle_summary = {
                "id": cycle["id"],
                "start_date": cycle["start_date"],
                "end_date": cycle["end_date"],
                "status": cycle["status"],
                "goals_count": cycle.get("goals_count", 0),
                "tasks_count": cycle.get("tasks_count", 0),
                "total_hours": cycle.get("total_hours", 0.0)
            }
            
            # Pokud je archivován, načti dodatečná data
            if cycle["status"] == "completed":
                archive = self.load_archive_cycle(cycle["id"])
                if archive:
                    # Přepočítej statistiky z dat
                    if archive.get("tasks"):
                        cycle_summary["tasks_count"] = len(archive["tasks"])
                        # Sečti hodiny
                        total_hours = sum(task[3] for task in archive["tasks"] if len(task) > 3)
                        cycle_summary["total_hours"] = total_hours
            
            summary.append(cycle_summary)
        
        return summary
    
    def needs_new_cycle(self):
        """
        Zkontroluje jestli je potřeba začít nový cyklus
        
        Returns:
            bool: True pokud uplynulo 12 týdnů od start_date aktivního cyklu
        """
        active = self.get_active_cycle()
        
        if not active:
            return True  # Žádný aktivní cyklus = potřeba vytvořit
        
        start_date = active["start_date"]
        today = datetime.now()
        
        days_since_start = (today - start_date).days
        
        return days_since_start >= 84  # 12 týdnů