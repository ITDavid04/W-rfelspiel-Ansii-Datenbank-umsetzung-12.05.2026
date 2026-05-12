# Wuerfel.py
import random

class Wuerfel:
    def __init__(self, name="Spieler", seiten=6, start_statistik=None):
        # 1. Namens-Validierung (Der "Guard")
        if not name.isalpha():
            self.name = "Unbekannt"
        else:
            self.name = name
            
        # 2. Diese Attribute müssen IMMER gesetzt werden (außerhalb vom else!)
        self.seiten = seiten
        self.statistik = start_statistik if start_statistik else [0] * seiten

    def rollen(self):
        wurf = random.randint(1, self.seiten)
        self.statistik[wurf - 1] += 1
        return wurf

    def get_gesamtanzahl(self):
        return sum(self.statistik)

    def zu_dict(self):
        return {"name": self.name, "statistik": self.statistik}