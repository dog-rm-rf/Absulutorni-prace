"""
Test archivace cyklu
"""

from models.cycles_manager import CyclesManager
from datetime import datetime


def test_archive():
    print("=" * 60)
    print("TEST ARCHIVACE CYKLU")
    print("=" * 60)
    
    # 1. Vytvoř CyclesManager
    print("\n1️⃣ Inicializace CyclesManager...")
    cm = CyclesManager()
    
    # 2. Zobraz aktivní cyklus
    print("\n2️⃣ Aktuální stav:")
    active = cm.get_active_cycle()
    
    if active:
        print(f"   Aktivní cyklus: #{active['id']}")
        print(f"   Start: {active['start_date'].date()}")
        print(f"   End: {active['end_date'].date()}")
        print(f"   Status: {active['status']}")
    else:
        print("   ⚠️ Žádný aktivní cyklus")
        print("   Nejdřív vytvoř cyklus spuštěním aplikace!")
        return
    
    # 3. Zkontroluj data v active/
    print("\n3️⃣ Kontrola dat v data/active/:")
    import os
    active_files = os.listdir("data/active/")
    if active_files:
        for f in active_files:
            print(f"   📄 {f}")
    else:
        print("   (žádné soubory)")
    
    # 4. Potvrď archivaci
    print("\n4️⃣ Archivace:")
    response = input("   Chceš archivovat tento cyklus? (ano/ne): ").strip().lower()
    
    if response not in ['ano', 'a', 'yes', 'y']:
        print("   ⏸️ Archivace zrušena")
        return
    
    # 5. Proveď archivaci
    print("\n   📦 Provádím archivaci...")
    success = cm.archive_current_cycle()
    
    if success:
        print("\n   ✅ Archivace dokončena!")
    else:
        print("\n   ❌ Archivace selhala")
        return
    
    # 6. Zkontroluj výsledek
    print("\n5️⃣ Kontrola výsledku:")
    
    # Zkontroluj archive/
    print("\n   📁 data/archive/:")
    archive_files = os.listdir("data/archive/")
    if archive_files:
        for f in archive_files:
            file_path = os.path.join("data/archive", f)
            size = os.path.getsize(file_path)
            print(f"   📦 {f} ({size} bytes)")
    else:
        print("   (žádné soubory)")
    
    # Zkontroluj active/
    print("\n   📁 data/active/:")
    active_files_after = os.listdir("data/active/")
    if active_files_after:
        for f in active_files_after:
            print(f"   📄 {f}")
    else:
        print("   ✅ (prázdné - správně vyčištěno)")
    
    # Zkontroluj metadata
    print("\n   📊 Metadata:")
    all_cycles = cm.get_all_cycles_summary()
    for cycle in all_cycles:
        status_emoji = "✅" if cycle['status'] == "active" else "📦"
        print(f"   {status_emoji} Cyklus #{cycle['id']}: {cycle['start_date'].date()} → {cycle['status']}")
        if cycle['status'] == "completed":
            if 'archive_file' in cycle:
                print(f"      Archive: {cycle['archive_file']}")
    
    # 7. Vytvoř nový cyklus?
    print("\n6️⃣ Nový cyklus:")
    response = input("   Chceš vytvořit nový cyklus? (ano/ne): ").strip().lower()
    
    if response in ['ano', 'a', 'yes', 'y']:
        new_cycle = cm.create_new_cycle()
        print(f"\n   ✅ Vytvořen cyklus #{new_cycle['id']}")
        print(f"   Start: {new_cycle['start_date'].date()}")
        print(f"   End: {new_cycle['end_date'].date()}")
    else:
        print("   ⏸️ Nový cyklus nevytvořen")
    
    print("\n" + "=" * 60)
    print("TEST DOKONČEN")
    print("=" * 60)


if __name__ == "__main__":
    test_archive()