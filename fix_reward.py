# fix_rewards.py
import pandas as pd
import os

file_path = "data/active/reward_dataframe.pkl"

if os.path.exists(file_path):
    # Načti starý DataFrame
    df = pd.read_pickle(file_path)
    
    print(f"Staré sloupce: {df.columns.tolist()}")
    print(f"Počet rewards: {len(df)}")
    
    # Přidej sloupec actual_time
    if 'actual_time' not in df.columns:
        # Zkopíruj hodnotu z 'time' sloupce
        df['actual_time'] = df['time']
        
        print(f"\n✅ Přidán sloupec 'actual_time'")
        print(f"Nové sloupce: {df.columns.tolist()}")
        
        # Ulož zpět
        df.to_pickle(file_path)
        print(f"\n✅ Soubor uložen: {file_path}")
    else:
        print("\n⚠️ Sloupec 'actual_time' už existuje")
else:
    print(f"❌ Soubor neexistuje: {file_path}")