import sqlite3
import json

class SQLiteRepository: # Diese Klasse verwaltet die Speicherung von Spielständen in einer SQLite-Datenbank
    def __init__(self, db_path="wuerfel_save.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self): # Initialisiert die Datenbank und erstellt die Tabelle, falls sie noch nicht existiert
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False) # check_same_thread=False ermöglicht die Nutzung der Verbindung in mehreren Threads, was für unser Spiel nützlich sein könnte
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS spielstaende (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                typ TEXT,
                daten TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """) # Die Tabelle "spielstaende" hat eine automatisch inkrementierende ID, einen Typ (z.B. "AUTOSAVE"), die gespeicherten Daten als JSON-String und einen Timestamp, der automatisch auf die aktuelle Zeit gesetzt wird
        self.conn.commit() # Änderungen an der Datenbank werden gespeichert

    def save_game(self, data: dict): # Speichert den Spielstand in der Datenbank, wobei data ein Dictionary mit den relevanten Informationen zum Spielstand ist
        if data is None: raise Exception("Keine Daten") # Für den Test-Rollback
        
        try: # Speichern des Spielstands in der Datenbank mit Transaktionssicherheit
            with self.conn: # 'with self.conn' startet automatisch eine Transaktion, sodass bei einem Fehler ein Rollback durchgeführt wird
                self.conn.execute(
                    "INSERT INTO spielstaende (typ, daten) VALUES (?, ?)",
                    ("TEST", json.dumps(data))
                ) # Die Daten werden als JSON-String gespeichert, um die komplexe Struktur des Spielstands zu erhalten. Der Typ wird hier als "TEST" gesetzt, könnte aber auch dynamisch sein.
        except Exception as e:
            raise e # Fehler nach oben reichen für den Test
        
    def leere_datenbank(self): # Löscht alle Einträge in der Tabelle "spielstaende", um die Datenbank zu leeren
        conn = sqlite3.connect(self.db_path)
        try:
            with conn: # 'with conn' startet automatisch eine Transaktion, sodass bei einem Fehler ein Rollback durchgeführt wird
                conn.execute("DELETE FROM spielstaende") # Alle Einträge in der Tabelle werden gelöscht, was die Datenbank effektiv leert
            print("✅ Datenbank erfolgreich geleert.")
            return True
        except sqlite3.Error as e:
            print(f"❌ Fehler beim Leeren: {e}")
            return False
        finally:
            conn.close() # Verbindung wird geschlossen, um Ressourcen freizugeben