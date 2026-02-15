import pandas as pd
from datetime import datetime

# Načti tasky
df = pd.read_pickle("data/active/tasks_dataframe.pkl")

print("=" * 60)
print("📊 ANALÝZA TASKŮ")
print("=" * 60)

print(f"\n📈 Celkový počet tasků: {len(df)}")

print("\n📅 Rozsah datumů:")
print(f"   První task: {df['date'].min()}")
print(f"   Poslední task: {df['date'].max()}")

print("\n🔍 První 5 tasků:")
print(df[['activity', 'date', 'desired_time_spent_hours']].head())

print("\n🔍 Posledních 5 tasků:")
print(df[['activity', 'date', 'desired_time_spent_hours']].tail())

print("\n📊 Tasky podle měsíců:")
df['month'] = df['date'].dt.strftime('%Y-%m')
print(df['month'].value_counts().sort_index())

print("\n" + "=" * 60)