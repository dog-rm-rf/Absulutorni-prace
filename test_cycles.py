"""
Test pro CyclesManager - ověření že funguje
"""

from models.cycles_manager import CyclesManager
from datetime import datetime


def test_cycles_manager():
    print("=" * 50)
    print("TEST CYCLES MANAGER")
    print("=" * 50)
    
    # 1. Vytvoř CyclesManager
    print("\n1️⃣ Vytváření CyclesManager...")
    cm = CyclesManager()
    
    # 2. Zjisti jestli existuje aktivní cyklus
    print("\n2️⃣ Kontrola aktivního cyklu...")
    active = cm.get_active_cycle()
    
    if active:
        print(f"   Aktivní cyklus: #{active['id']}")
        print(f"   Start: {active['start_date'].date()}")
        print(f"   End: {active['end_date'].date()}")
    else:
        print("   ⚠️ Žádný aktivní cyklus")
    
    # 3. Potřebujeme nový cyklus?
    print("\n3️⃣ Potřebujeme nový cyklus?")
    needs_new = cm.needs_new_cycle()
    print(f"   needs_new_cycle() = {needs_new}")
    
    # 4. Pokud potřebujeme, vytvoř nový
    if needs_new:
        print("\n4️⃣ Vytváření nového cyklu...")
        new_cycle = cm.create_new_cycle()
        print(f"   ✅ Vytvořen cyklus #{new_cycle['id']}")
    else:
        print("\n4️⃣ Cyklus už existuje, nevytvářím nový")
    
    # 5. Zobraz všechny cykly
    print("\n5️⃣ Všechny cykly:")
    summary = cm.get_all_cycles_summary()
    
    if summary:
        for cycle in summary:
            status_emoji = "✅" if cycle['status'] == "active" else "📦"
            print(f"   {status_emoji} Cyklus #{cycle['id']}: {cycle['start_date'].date()} → {cycle['status']}")
    else:
        print("   (žádné cykly)")
    
    # 6. Test archivace (NEPOVINNÉ - zakomentované)
    # print("\n6️⃣ Test archivace (pro test, pak smaž)...")
    # cm.archive_current_cycle()
    
    print("\n" + "=" * 50)
    print("TEST DOKONČEN")
    print("=" * 50)


if __name__ == "__main__":
    test_cycles_manager()