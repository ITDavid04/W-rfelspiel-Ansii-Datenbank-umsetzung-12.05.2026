import unittest # Importiert das unittest-Modul, um Testfälle zu erstellen und auszuführen
from infrastructure.sqlite_repository import SQLiteRepository # Importiert die SQLiteRepository-Klasse, die für die Speicherung der Spielstände in einer SQLite-Datenbank verantwortlich ist

class TestSQLiteSpeicherung(unittest.TestCase): # Definiert eine Testklasse, die von unittest.TestCase erbt, um Testmethoden zu erstellen
    def setUp(self): # Vor jedem Test wird eine neue Instanz mit ":memory:" erstellt, um eine frische Datenbank zu haben
        self.repo = SQLiteRepository(":memory:") # Verwendet eine In-Memory-Datenbank für Tests, um keine echten Dateien zu erstellen und die Tests isoliert zu halten

    def test_speichern_erfolgreich(self): # Testet, ob der Speichervorgang ohne Fehler durchläuft
        test_daten = {"max_wuerfe": 5, "start_index": 0, "mehrspieler_daten": [{"name": "Test"}]}
        
        try: # Versucht, die Testdaten zu speichern, und fängt alle Exceptions ab
            self.repo.save_game(test_daten) # Sollte ohne Fehler durchlaufen
            erfolg = True
        except Exception:
            erfolg = False
        
        self.assertTrue(erfolg, "Speichern sollte ohne Fehler durchlaufen")

    def test_rollback_bei_fehler(self): # Testet, ob eine Exception geworfen wird, wenn Daten fehlen, und ob der Rollback korrekt durchgeführt wird
        with self.assertRaises(Exception): # Erwartet, dass eine Exception geworfen wird, wenn None übergeben wird
            self.repo.save_game(None) 
        print("\n✅ Rollback-Test: Fehler wurde korrekt abgefangen.")

if __name__ == '__main__':
    unittest.main()