
from infrastructure.file_managerDavid import save_data, load_data, SaveFormat # Importieren der Funktionen und Klassen aus dem File-Manager-Modul
from infrastructure.style_config import GOLD, RESET, FETT
from rangliste_service import erstelle_rangliste

def sichere_spielstand(alle_wuerfel, max_wuerfe, spieler_index, typ="AUTOSAVE"):
    dateiname = f"wuerfel_projekt_{typ}" # Erzeugt z.B. wuerfel_projekt_AUTOSAVE
    zustand = {
        "mehrspieler_daten": [w.zu_dict() for w in alle_wuerfel],
        "max_wuerfe": max_wuerfe,
        "naechster_spieler_index": spieler_index
    }
    save_data(zustand, dateiname, SaveFormat.JSON)
    return True

def lade_spielstand_aufbereitet(gewaehlte_datei, format_typ):# Diese Funktion lädt die Spieldaten und bereitet sie für das Hauptprogramm auf
    daten = load_data(gewaehlte_datei, format_typ)# Laden der Daten mit dem File-Manager, basierend auf dem angegebenen Format
    
    if not daten or "mehrspieler_daten" not in daten:# Überprüfung, ob die Daten gültig sind und die erwarteten Felder enthalten
        return None

    # Hier extrahieren wir die max_wuerfe und den start_index, falls sie im geladenen Daten vorhanden sind, ansonsten setzen wir Standardwerte  
    max_wuerfe = daten.get("max_wuerfe", 30)  # Standardwert 30, falls Feld fehlt
    start_index = daten.get("naechster_spieler_index", 0)# Standardwert 0, falls Feld fehlt
    
    # Wir geben ein Dictionary zurück, damit das Hauptprogramm alles auf einmal hat
    return {
        "rohdaten": daten["mehrspieler_daten"],
        "max_wuerfe": max_wuerfe,
        "start_index": start_index}
    
    
def zeige_tabellen_ansicht(aktuelle_rangliste):
    """
    Nimmt eine Liste von Tupeln [(Name, Punkte), ...] entgegen
    und gibt sie formatiert als Tabelle aus.
    """
    print(f"\n{FETT}📊 AKTUELLE RANGLISTE{RESET}")
    
    for platz, (name, punkte) in enumerate(aktuelle_rangliste, start=1):
        # Optik-Logik: Gold für Platz 1
        farbe = GOLD if platz == 1 else RESET
        
        # Die Formatierung mit :<12 und :>3 bleibt hier, da sie zur Anzeige gehört
        print(f"{farbe}Platz {platz}: {name:<12} | {punkte:>3} Punkte{RESET}")    
        
def zeige_runden_header(runde, max_wuerfe):
    """
    Gibt die aktuelle Runde und die Anzahl der verbleibenden Würfe aus.
    """
    print(f"\n{FETT}--- RUNDE {runde} (Verfügbare Würfe: {max_wuerfe}) ---{RESET}")
    
def zeige_rangliste(alle_wuerfel):
    """
    Kombiniert die Logik: Erstellt die Rangliste aus den Objekten 
    und gibt sie dann als Tabelle aus.
    """
    # 1. Daten verarbeiten (Logik aus rangliste_service)
    rangliste = erstelle_rangliste(alle_wuerfel)
    
    # 2. Daten anzeigen (Funktion von oben im gleichen Modul)
    zeige_tabellen_ansicht(rangliste)    
        