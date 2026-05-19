import sqlite3
import json
from application.rangliste_service import erstelle_rangliste
from infrastructure.style_config import GOLD, RESET, FETT

# --- KONFIGURATION ---
DB_NAME = "wuerfel_save.db"

def _init_db():
    """Erstellt die Tabelle, falls sie noch nicht existiert."""
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS spielstaende (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                typ TEXT,
                daten TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

# Initialisierung beim Laden des Moduls
_init_db()

def sichere_spielstand(alle_wuerfel, max_wuerfe, spieler_index, typ="AUTOSAVE"):
    """Speichert den Spielstand mit Transaktionssicherheit und Rollback."""
    zustand = {
        "mehrspieler_daten": [w.zu_dict() for w in alle_wuerfel],
        "max_wuerfe": max_wuerfe,
        "naechster_spieler_index": spieler_index
    }
    
    conn = sqlite3.connect(DB_NAME)
    try:
        # 'with conn' startet automatisch eine Transaktion
        with conn:
            conn.execute(
                "INSERT INTO spielstaende (typ, daten) VALUES (?, ?)",
                (typ, json.dumps(zustand))
            )
        print(f"\n✅ Spielstand ({typ}) wurde erfolgreich in der Datenbank gespeichert.")
        return True
    except sqlite3.Error as e:
        # Bei Fehlern wird durch den 'with'-Block automatisch ein Rollback ausgeführt
        print(f"\n❌ FEHLER beim Speichern: {e}")
        print("⚠️ Rollback wurde durchgeführt – keine korrupten Daten wurden gespeichert.")
        return False
    finally:
        conn.close()

def zeige_tabellen_ansicht(aktuelle_rangliste):
    print(f"\n{FETT}📊 AKTUELLE RANGLISTE{RESET}")
    for platz, (name, punkte) in enumerate(aktuelle_rangliste, start=1):
        farbe = GOLD if platz == 1 else RESET
        print(f"{farbe}Platz {platz}: {name:<12} | {punkte:>3} Punkte{RESET}")    
    
def zeige_runden_header(runde, max_wuerfe):
    print(f"\n{FETT}--- RUNDE {runde} (Verfügbare Würfe: {max_wuerfe}) ---{RESET}")
    
def zeige_rangliste(alle_wuerfel):
    rangliste = erstelle_rangliste(alle_wuerfel)
    zeige_tabellen_ansicht(rangliste)