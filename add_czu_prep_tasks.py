# -*- coding: utf-8 -*-
"""
Maximální plán přípravy na CZU - Informatika 2026
"""

from datetime import datetime, timedelta
from models.all_tasks import All_tasks

# ===== KONFIGURACE =====
START_DATE      = datetime(2026, 2, 11)
PRIJIMACKY_DATE = datetime(2026, 6, 15)
FAZE_1_END      = datetime(2026, 4, 1)
FAZE_2_END      = datetime(2026, 6, 1)

# ===== OBSAHY =====

MATH_FAZE1 = [
    "Rovnice - lineární a kvadratické",
    "Nerovnice a soustavy nerovnic",
    "Funkce - definice, vlastnosti, graf",
    "Lineární a kvadratická funkce",
    "Exponenciální funkce a rovnice",
    "Logaritmická funkce a rovnice",
    "Goniometrie - sin, cos, tan a grafy",
    "Goniometrie - základní vzorce a rovnice",
    "Kombinatorika - permutace, variace, kombinace",
    "Pravděpodobnost - základy a příklady",
]

MATH_FAZE2 = [
    "Rovnice a nerovnice - těžké příklady",
    "Funkce - transformace a složené funkce",
    "Exponenciální a log. rovnice - pokročilé",
    "Goniometrie - rovnice a soustavy",
    "Goniometrie - součtové a dvojnásobné vzorce",
    "Kombinatorika a pravděpodobnost - složitější",
    "Podmíněná pravděpodobnost",
    "Posloupnosti - aritmetické a geometrické",
    "Finanční matematika - úroky a splátky",
    "Analytická geometrie - přímka a kružnice",
    "Analytická geometrie - vzdálenosti a průsečíky",
    "Komplexní čísla - základy",
    "Derivace - definice a základní pravidla",
    "Integrály - Newton-Leibnizova formule",
    "Vzorový test CZU - celý na čas",
]

ENGLISH = [
    "Present Simple vs Continuous",
    "Past Simple vs Past Continuous",
    "Present Perfect vs Past Simple",
    "Past Perfect",
    "Future tenses - will, going to",
    "Podmínkové věty 0, 1, 2, 3",
    "Nepřímá řeč - oznamovací věty",
    "Nepřímá řeč - otázky a rozkazy",
    "Trpný rod - všechny časy",
    "Modální slovesa - can, could, may, might",
    "Modální slovesa - must, have to, should",
    "Předložky místa, času a způsobu",
    "Phrasal verbs",
    "Relative clauses",
    "Gerund vs Infinitive",
    "Reading comprehension - tech articles (B2)",
    "Listening - TED talks",
    "Writing - essay a email struktura",
    "Vocabulary - IT terminologie",
    "Vzorový test CZU - angličtina na čas",
]

# Python - systematicky od základů po pokročilé
# Každé téma = 1 session (čti + piš kód + procvič)
PYTHON = [
    # === ZÁKLADY ===
    "Python základy - proměnné, datové typy (int, float, str, bool)",
    "Python základy - podmínky if/elif/else, porovnávání",
    "Python základy - cyklus for, range, iterace přes seznam",
    "Python základy - cyklus while, break, continue",
    "Python základy - funkce: def, parametry, return, scope",
    "Python základy - výchozí parametry, *args, **kwargs",
    "Python základy - seznam (list): indexování, slicing, metody",
    "Python základy - slovník (dict): klíče, hodnoty, iterace",
    "Python základy - n-tice (tuple) a množiny (set)",
    "Python základy - řetězce: f-strings, metody, split/join",
    "Python základy - soubory: open, read, write, with",
    "Python základy - výjimky: try/except/finally, vlastní výjimky",
    "Python základy - moduly: import, from, __name__",
    "Python základy - list comprehension a dict comprehension",
    # === OOP ===
    "Python OOP - třídy, objekty, __init__, self",
    "Python OOP - metody instance vs třídní vs statické",
    "Python OOP - dědičnost, super(), přepisování metod",
    "Python OOP - magické metody: __str__, __repr__, __len__, __eq__",
    "Python OOP - properties, gettery a settery",
    "Python OOP - abstraktní třídy a rozhraní (abc modul)",
    "Python OOP - datové třídy (dataclasses)",
    # === POKROČILÉ KONCEPTY ===
    "Python pokročilé - lambda, map, filter, zip",
    "Python pokročilé - generátory a yield",
    "Python pokročilé - dekorátory - co jsou, jak fungují, vlastní",
    "Python pokročilé - context managers a protokol __enter__/__exit__",
    "Python pokročilé - iterátory a iterovatelné objekty",
    "Python pokročilé - type hints a anotace (mypy)",
    "Python pokročilé - funkcionální programování - reduce, partial",
    "Python pokročilé - regulární výrazy (re modul)",
    "Python pokročilé - datetime, os, pathlib moduly",
    "Python pokročilé - logging modul - správné logování",
    "Python pokročilé - virtual environments a správa závislostí",
    "Python pokročilé - unit testy (pytest) - základy",
    "Python pokročilé - unit testy - fixtures, parametrize, mocking",
    "Python pokročilé - async/await a asyncio základy",
    # === PRAKTICKÉ DOVEDNOSTI ===
    "Python praxe - práce s JSON a CSV (json, csv moduly)",
    "Python praxe - HTTP requesty (requests knihovna)",
    "Python praxe - web scraping (BeautifulSoup základy)",
    "Python praxe - SQLite v Pythonu (sqlite3 modul)",
    "Python praxe - pandas - načtení dat, základní operace",
    "Python praxe - pandas - groupby, merge, pivot",
    "Python praxe - mini projekt: CLI správce úkolů",
    "Python praxe - mini projekt: web scraper článků",
    "Python praxe - mini projekt: REST API klient",
    "Python praxe - mini projekt: analýza dat z CSV",
]

# LeetCode / kódovací úlohy - od easy po medium
LEETCODE = [
    # Easy - základní logika
    "LeetCode Easy - Two Sum (arrays, hash map)",
    "LeetCode Easy - Reverse String (strings)",
    "LeetCode Easy - FizzBuzz (základní logika)",
    "LeetCode Easy - Palindrome Number",
    "LeetCode Easy - Valid Anagram (string, dict)",
    "LeetCode Easy - Contains Duplicate (set)",
    "LeetCode Easy - Maximum Subarray (Kadane)",
    "LeetCode Easy - Merge Sorted Array",
    "LeetCode Easy - Best Time to Buy/Sell Stock",
    "LeetCode Easy - Climbing Stairs (rekurze/DP)",
    "LeetCode Easy - Linked List Cycle",
    "LeetCode Easy - Valid Parentheses (stack)",
    "LeetCode Easy - Binary Search",
    "LeetCode Easy - First Bad Version",
    "LeetCode Easy - Ransom Note (dict)",
    # Medium - složitější myšlení
    "LeetCode Medium - 3Sum (two pointers)",
    "LeetCode Medium - Product of Array Except Self",
    "LeetCode Medium - Group Anagrams",
    "LeetCode Medium - Longest Substring Without Repeating",
    "LeetCode Medium - Container With Most Water",
    "LeetCode Medium - Top K Frequent Elements",
    "LeetCode Medium - Valid Sudoku",
    "LeetCode Medium - Coin Change (DP)",
    "LeetCode Medium - Number of Islands (BFS/DFS)",
    "LeetCode Medium - Course Schedule (grafy)",
]

SQL = [
    "SQL - SELECT, FROM, WHERE základy",
    "SQL - ORDER BY, LIMIT, DISTINCT",
    "SQL - agregace: COUNT, SUM, AVG, MIN, MAX",
    "SQL - GROUP BY a HAVING",
    "SQL - INNER JOIN a LEFT JOIN",
    "SQL - RIGHT JOIN, FULL JOIN, SELF JOIN",
    "SQL - poddotazy (subqueries)",
    "SQL - INSERT, UPDATE, DELETE",
    "SQL - CREATE TABLE, datové typy, PRIMARY KEY",
    "SQL - indexy, výkon a EXPLAIN",
    "SQL - Python + SQLite projekt",
    "SQL - HackerRank SQL challenges (easy)",
]

LINUX = [
    "Linux - základní příkazy: ls, cd, pwd, mkdir, rm, cp, mv",
    "Linux - práce s textem: cat, grep, sed, awk, less",
    "Linux - oprávnění: chmod, chown, sudo, groups",
    "Linux - procesy: ps, top, htop, kill, bg, fg, &",
    "Linux - balíčky: apt, pip, snap",
    "Linux - shell scripting: proměnné, podmínky, cykly",
    "Linux - shell scripting: funkce, vstup/výstup, praktický skript",
    "Linux - síťové příkazy: ping, curl, wget, ss, nmap",
]

GIT = [
    "Git - init, status, add, commit, log",
    "Git - větve: branch, checkout, merge",
    "Git - GitHub: push, pull, clone, fork, PR",
    "Git - řešení konfliktů při merge",
    "Git - rebase, stash, cherry-pick",
    "Git - workflow pro projekty (feature branches, conventional commits)",
]

NETWORKS = [
    "Sítě - OSI model, IP adresy, masky, porty",
    "Sítě - TCP vs UDP, DNS, DHCP, NAT",
    "Sítě - HTTP - metody, hlavičky, status kódy",
    "Sítě - REST API - principy, JSON, autentizace",
    "Sítě - HTTPS a základy šifrování (TLS, certifikáty)",
    "Sítě - prakticky: curl, Postman, HTTP v Pythonu",
]

ALGO = [
    "Algoritmy - Big O notace: O(1), O(n), O(n²), O(log n)",
    "Algoritmy - lineární vs binární vyhledávání",
    "Datové struktury - Stack a Queue (implementace v Pythonu)",
    "Datové struktury - Linked List (jednosměrný, obousměrný)",
    "Datové struktury - Binary Search Tree",
    "Algoritmy - Bubble, Selection, Insertion sort",
    "Algoritmy - Merge sort a Quick sort",
    "Datové struktury - Hash tabulky a kolize",
    "Algoritmy - rekurze: faktoriál, Fibonacci, Hanoi",
    "Algoritmy - dynamické programování základy",
    "Algoritmy - grafy: reprezentace, BFS, DFS",
    "Algoritmy - Dijkstrův algoritmus",
]

BOOKS = [
    # Python začátečník - nejlepší volba
    "Automate the Boring Stuff (kap. 1-2) - základy",
    "Automate the Boring Stuff (kap. 3-4) - lists, dicts",
    "Automate the Boring Stuff (kap. 5-6) - soubory a regex",
    "Automate the Boring Stuff (kap. 7-8) - web a PDF",
    # Čistý kód
    "Clean Code (kap. 1-2) - proč na kódu záleží",
    "Clean Code (kap. 3-4) - funkce a komentáře",
    "Clean Code (kap. 5-6) - formátování a objekty",
    "Clean Code (kap. 7-8) - error handling",
    # CS základ
    "Computer Science Distilled (kap. 1-2) - základy myšlení",
    "Computer Science Distilled (kap. 3-4) - algoritmy",
    "Computer Science Distilled (kap. 5-6) - datové struktury",
    "Computer Science Distilled (kap. 7-8) - databáze a sítě",
    # Pragmatický přístup
    "The Pragmatic Programmer (kap. 1-2) - filozofie",
    "The Pragmatic Programmer (kap. 3-4) - nástroje a debugging",
    "The Pragmatic Programmer (kap. 5-6) - přizpůsobivý kód",
    # Bonusové
    "Cracking the Coding Interview - úvod a Big O kapitola",
    "Cracking the Coding Interview - Arrays & Strings kapitola",
]

# ===== HELPER =====

def add(at, name, subclass, date, hours):
    at.add_new_task([name, subclass, date, hours, None, ["", "", ""]])

# ===== FÁZE 1 =====

def generate_faze_1(at):
    print("\n  Fáze 1 (11.2. - 1.4.2026)")

    current = START_DATE
    mi = ei = bi = pi = lc = gi = ai = 0
    count = 0

    while current <= FAZE_1_END:
        dow = current.weekday()

        # Cvičení každý den
        add(at, "Cvičit", "cvičení", current, 0.25)
        count += 1

        # Knihy každý den 30 min
        add(at, f"Čtení - {BOOKS[bi % len(BOOKS)]}", "knihy", current, 0.5)
        bi += 1
        count += 1

        if dow < 3:  # Po, Út, St - absolutorky 8h
            add(at, "Absolutorní práce", "škola", current, 8.0)
            # LeetCode večer - mozek už nepojme víc
            add(at, f"{LEETCODE[lc % len(LEETCODE)]}", "leetcode", current, 1.0)
            lc += 1
            count += 2

        elif dow == 3:  # Čt
            add(at, "Absolutorní práce", "škola", current, 4.0)
            add(at, f"Matematika - {MATH_FAZE1[mi % len(MATH_FAZE1)]}", "matematika", current, 1.5)
            mi += 1
            add(at, f"Angličtina - {ENGLISH[ei % len(ENGLISH)]}", "angličtina", current, 1.0)
            ei += 1
            add(at, f"Python - {PYTHON[pi % len(PYTHON)]}", "python", current, 1.0)
            pi += 1
            count += 4

        elif dow == 4:  # Pá
            add(at, f"Matematika - {MATH_FAZE1[mi % len(MATH_FAZE1)]}", "matematika", current, 2.0)
            mi += 1
            add(at, f"Angličtina - {ENGLISH[ei % len(ENGLISH)]}", "angličtina", current, 1.5)
            ei += 1
            add(at, f"Python - {PYTHON[pi % len(PYTHON)]}", "python", current, 1.5)
            pi += 1
            add(at, f"{LEETCODE[lc % len(LEETCODE)]}", "leetcode", current, 1.0)
            lc += 1
            count += 4

        elif dow == 5:  # So
            add(at, f"Matematika - vzorové příklady + {MATH_FAZE1[mi % len(MATH_FAZE1)]}", "matematika", current, 2.5)
            mi += 1
            add(at, f"Python - {PYTHON[pi % len(PYTHON)]}", "python", current, 2.0)
            pi += 1
            add(at, f"Git - {GIT[gi % len(GIT)]}", "git", current, 1.0)
            gi += 1
            add(at, f"Algoritmy - {ALGO[ai % len(ALGO)]}", "algoritmy", current, 1.0)
            ai += 1
            count += 4

        elif dow == 6:  # Ne
            add(at, f"Angličtina - {ENGLISH[ei % len(ENGLISH)]}", "angličtina", current, 2.0)
            ei += 1
            add(at, f"Python - {PYTHON[pi % len(PYTHON)]}", "python", current, 2.0)
            pi += 1
            add(at, f"{LEETCODE[lc % len(LEETCODE)]}", "leetcode", current, 1.0)
            lc += 1
            add(at, f"Algoritmy - {ALGO[ai % len(ALGO)]}", "algoritmy", current, 1.0)
            ai += 1
            count += 4

        current += timedelta(days=1)

    print(f"     ✅ {count} tasků")
    return dict(mi=mi, ei=ei, bi=bi, pi=pi, lc=lc, gi=gi, ai=ai,
                si=0, li=0, ni=0, gym_i=0)

# ===== FÁZE 2 =====

def generate_faze_2(at, idxs):
    print("\n  Fáze 2 (1.4. - 1.6.2026)")

    current = FAZE_2_END - (FAZE_2_END - (FAZE_1_END + timedelta(days=1)))
    current = FAZE_1_END + timedelta(days=1)
    mi = idxs["mi"]; ei = idxs["ei"]; bi = idxs["bi"]
    pi = idxs["pi"]; lc = idxs["lc"]; gi = idxs["gi"]
    ai = idxs["ai"]; si = idxs["si"]; li = idxs["li"]; ni = idxs["ni"]
    week = 1
    count = 0

    while current <= FAZE_2_END:
        dow = current.weekday()

        add(at, "Cvičit", "cvičení", current, 0.25)
        add(at, f"Čtení - {BOOKS[bi % len(BOOKS)]}", "knihy", current, 0.5)
        bi += 1
        count += 2

        if dow == 0:  # Po - matika + Python + LeetCode
            add(at, f"Matematika - {MATH_FAZE2[mi % len(MATH_FAZE2)]}", "matematika", current, 3.0)
            mi += 1
            add(at, f"Python - {PYTHON[pi % len(PYTHON)]}", "python", current, 2.0)
            pi += 1
            add(at, f"{LEETCODE[lc % len(LEETCODE)]}", "leetcode", current, 1.0)
            lc += 1
            count += 3

        elif dow == 1:  # Út - matika + SQL + AJ
            add(at, f"Matematika - {MATH_FAZE2[mi % len(MATH_FAZE2)]}", "matematika", current, 3.0)
            mi += 1
            add(at, f"SQL - {SQL[si % len(SQL)]}", "sql", current, 1.5)
            si += 1
            add(at, f"Angličtina - {ENGLISH[ei % len(ENGLISH)]}", "angličtina", current, 1.5)
            ei += 1
            count += 3

        elif dow == 2:  # St - matika + Linux + LeetCode
            add(at, f"Matematika - {MATH_FAZE2[mi % len(MATH_FAZE2)]}", "matematika", current, 3.0)
            mi += 1
            add(at, f"Linux - {LINUX[li % len(LINUX)]}", "linux", current, 1.5)
            li += 1
            add(at, f"{LEETCODE[lc % len(LEETCODE)]}", "leetcode", current, 1.0)
            lc += 1
            count += 3

        elif dow == 3:  # Čt - matika + Sítě + AJ
            add(at, f"Matematika - {MATH_FAZE2[mi % len(MATH_FAZE2)]}", "matematika", current, 3.0)
            mi += 1
            add(at, f"Sítě - {NETWORKS[ni % len(NETWORKS)]}", "sítě", current, 1.5)
            ni += 1
            add(at, f"Angličtina - {ENGLISH[ei % len(ENGLISH)]}", "angličtina", current, 1.5)
            ei += 1
            count += 3

        elif dow == 4:  # Pá - matika + Algoritmy + Python
            add(at, f"Matematika - {MATH_FAZE2[mi % len(MATH_FAZE2)]}", "matematika", current, 2.5)
            mi += 1
            add(at, f"Algoritmy - {ALGO[ai % len(ALGO)]}", "algoritmy", current, 1.5)
            ai += 1
            add(at, f"Python - {PYTHON[pi % len(PYTHON)]}", "python", current, 1.5)
            pi += 1
            count += 3

        elif dow == 5:  # So - SIMULACE + Python projekt + Git
            add(at, f"SIMULOVANÝ TEST - Matematika (týden {week})", "test", current, 2.5)
            add(at, f"SIMULOVANÝ TEST - Angličtina (týden {week})", "test", current, 1.5)
            add(at, f"Python - {PYTHON[pi % len(PYTHON)]}", "python", current, 2.0)
            pi += 1
            add(at, f"Git - {GIT[gi % len(GIT)]}", "git", current, 0.5)
            gi += 1
            count += 4

        elif dow == 6:  # Ne - Review + AJ + LeetCode + Algoritmy
            add(at, f"Review týdne {week} - analýza chyb, slabá témata", "review", current, 1.5)
            add(at, f"Angličtina - {ENGLISH[ei % len(ENGLISH)]}", "angličtina", current, 1.5)
            ei += 1
            add(at, f"{LEETCODE[lc % len(LEETCODE)]}", "leetcode", current, 1.0)
            lc += 1
            add(at, f"Algoritmy - {ALGO[ai % len(ALGO)]}", "algoritmy", current, 1.0)
            ai += 1
            week += 1
            count += 4

        current += timedelta(days=1)

    print(f"     ✅ {count} tasků")
    return dict(mi=mi, ei=ei, bi=bi, pi=pi, lc=lc, gi=gi, ai=ai,
                si=si, li=li, ni=ni)

# ===== FÁZE 3 =====

def generate_faze_3(at, idxs):
    print("\n  Fáze 3 (1.6. - 15.6.2026)")

    current = FAZE_2_END + timedelta(days=1)
    mi = idxs["mi"]; ei = idxs["ei"]; bi = idxs["bi"]
    lc = idxs["lc"]
    count = 0

    while current <= PRIJIMACKY_DATE:
        dow = current.weekday()

        add(at, "Cvičit", "cvičení", current, 0.25)
        add(at, f"Čtení - {BOOKS[bi % len(BOOKS)]}", "knihy", current, 0.5)
        bi += 1
        count += 2

        if dow < 5:
            add(at, f"Matematika - opakování + {MATH_FAZE2[mi % len(MATH_FAZE2)]}", "matematika", current, 2.5)
            mi += 1
            add(at, f"Angličtina - {ENGLISH[ei % len(ENGLISH)]}", "angličtina", current, 1.5)
            ei += 1
            add(at, f"{LEETCODE[lc % len(LEETCODE)]}", "leetcode", current, 1.0)
            lc += 1
            add(at, "Mentální příprava - vizualizace, projdi si co umíš", "mindset", current, 0.25)
            count += 4

        elif dow == 5:
            add(at, "FULL SIMULACE - Matika + Angličtina, reálné podmínky", "test", current, 4.0)
            add(at, "Analýza simulace - co šlo špatně", "review", current, 1.0)
            count += 2

        elif dow == 6:
            add(at, "Lehké opakování - vzorce a slovíčka", "review", current, 1.0)
            add(at, "Odpočinek", "mindset", current, 0.25)
            count += 2

        current += timedelta(days=1)

    print(f"     ✅ {count} tasků")

# ===== SETUP =====

def add_setup(at):
    print("\n  Setup tasky")
    tasks = [
        ("Stáhnout vzorové příklady matika z CZU",           "příprava",   START_DATE,                    0.25),
        ("Stáhnout vzorové otázky angličtina z CZU",          "příprava",   START_DATE,                    0.25),
        ("Projít vzorové příklady matika - označit co nevím", "matematika", START_DATE + timedelta(days=1), 2.0),
        ("Projít vzorové otázky AJ - označit co nevím",       "angličtina", START_DATE + timedelta(days=1), 1.0),
        ("Nastavit Anki deck pro anglická slovíčka",          "angličtina", START_DATE + timedelta(days=2), 0.5),
        ("Vytvořit účet na LeetCode",                         "leetcode",   START_DATE + timedelta(days=2), 0.25),
        ("Nainstalovat Python, VS Code, git",                 "python",     START_DATE + timedelta(days=2), 0.5),
        ("Stáhnout Automate the Boring Stuff (free online)",  "knihy",      START_DATE + timedelta(days=2), 0.25),
        ("Stáhnout/sehnat Clean Code",                        "knihy",      START_DATE + timedelta(days=2), 0.25),
        ("Sepsat seznam slabých témat z matiky a AJ",         "příprava",   START_DATE + timedelta(days=3), 1.0),
    ]
    for name, subclass, date, hours in tasks:
        add(at, name, subclass, date, hours)
    print(f"     ✅ {len(tasks)} tasků")

# ===== MAIN =====

def main():
    print("=" * 65)
    print("  MAXIMALNI PLAN - CZU INFORMATIKA 2026")
    print("=" * 65)
    print(f"  Start:      {START_DATE.strftime('%d.%m.%Y')}")
    print(f"  Prijimacky: {PRIJIMACKY_DATE.strftime('%d.%m.%Y')}")
    print(f"  Zbyvá:      {(PRIJIMACKY_DATE - START_DATE).days} dní\n")
    print("  Každý den: cvičení + 30 min čtení knihy\n")
    print("  FÁZE 1 (do absolutorek):")
    print("    Po-St: absolutorky 8h + LeetCode večer")
    print("    Čt:    absolutorky 4h + matika + AJ + Python")
    print("    Pá:    matika + AJ + Python + LeetCode")
    print("    So:    matika + Python + Git + Algoritmy")
    print("    Ne:    AJ + Python + LeetCode + Algoritmy\n")
    print("  FÁZE 2 (intenzivní):")
    print("    Po: matika + Python + LeetCode")
    print("    Út: matika + SQL + AJ")
    print("    St: matika + Linux + LeetCode")
    print("    Čt: matika + Sítě + AJ")
    print("    Pá: matika + Algoritmy + Python")
    print("    So: SIMULACE + Python projekt + Git")
    print("    Ne: Review + AJ + LeetCode + Algoritmy\n")
    print("  FÁZE 3 (finální):")
    print("    Po-Pá: opakování + AJ + LeetCode + mindset")
    print("    So: FULL simulace")
    print("    Ne: lehké opakování + odpočinek")
    print("=" * 65)

    at = All_tasks()
    initial = len(at.list_of_all_tasks_objects)
    print(f"\n  Aktuální počet tasků: {initial}")
    print("\n  POZOR: Skript přidá ~800+ tasků.")
    resp = input("  Pokračovat? (ano/ne): ").lower().strip()
    if resp != "ano":
        print("  Zrušeno.")
        return

    print("\nGeneruji...\n")
    add_setup(at)
    idxs = generate_faze_1(at)
    idxs = generate_faze_2(at, idxs)
    generate_faze_3(at, idxs)

    final = len(at.list_of_all_tasks_objects)
    df = at.data_frame
    print("\n" + "=" * 65)
    print("  HOTOVO!")
    print("=" * 65)
    print(f"  Přidáno: {final - initial} tasků")
    print(f"  Celkem:  {final} tasků\n")
    print("  Breakdown:")
    print(df['task_sub_class'].value_counts().to_string())
    print("\n  Makej. Dostanes se tam!")

if __name__ == "__main__":
    main()