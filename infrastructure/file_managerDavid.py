#universeller filemanager als Werkzeugkasten 
import json #ermöglicht das speichern und laden von .json Datein
import yaml # siehe .json
from enum import Enum
from typing import Any
import os #Brücke zwischen Code und Betriebssystem/ kann Ordner erstellen, Dateien löschen, Dateien Umbenennen etc
import xml.etree.ElementTree as ET
import datetime #Importieren von datetime um gespicherte Datein mit Zeitstempel zu versehen

class SaveFormat(Enum):#Definition der unterstützten Speicherformate
    JSON = "json"
    YAML = "yaml"
    XML = "xml"

def save_data(data: dict[str, Any], base_filename: str, format_type: SaveFormat) -> None:
    """Universelle Funktion zum Speichern von Dictionaries."""
    #da wir unsere speicherdaten in einem serperaten ordner lagern nwollen müssen wir den pfad anpassen
    # Dateiendung automatisch anhängen (kleingeschrieben) / Hinzufügen eines Zeitstempels
    save_folder = "saves"
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        
    
    zeitstempel = datetime.datetime.now().strftime("%Y%m%d_%H%M")# Klammer sagt z.B. %Y = Year %m = month etc. / man könnte auch sekunden hinzufügen aber das wäre nicht "Hübsch" als ergebnis würde der if block rausfliegen
    
    filename_ohne_pfad = f"{base_filename}_{zeitstempel}.{format_type.value.lower()}"# Kombiniert den Basisnamen, den Zeitstempel und die Dateiendung aus dem Enum/ Generiert den Dateinamen ohne Pfadangabe
    full_path = os.path.join(save_folder, filename_ohne_pfad)## .value greift auf den String zu
    #durc hden Zeitstempel mit angabe Minuten sollte es nicht zu einer Überschreibung kommen es sei den es wird 2 mal in der selben Minute gespeichert
    #falls dies doch geschiet sicher wir es durch  if os.path.exists(full_path) ab. Das Script fragt ob es die Datein im Ordner schon gibt
    if os.path.exists(full_path):
        sekunden =datetime.datetime.now().strftime("%S")#wir fügen hier sekunden im zeitstempel ein falls 2 mal in der selben minute gespeichert wird
        filename_ohne_pfad= f"{base_filename}_{zeitstempel}_{sekunden}.{format_type.value.lower()}"# .value greift auf den String zu / dateiname mit Sekunden-Erweiterung neu generieren (z.B. ..._1036_18.json)
        full_path = os.path.join(save_folder, filename_ohne_pfad)# den vollständigen Pfad mit dem neuen Dateinamen aktualisieren 
        
    try:
        #später würde hier noch stehen encoding='utf-8' um fehler auszuschliessen und nur dieses Format zuzulassen/ encoding='Utf-8' hinzugefügt
        match format_type:
            case SaveFormat.JSON:
                with open(full_path, 'w', encoding='utf-8') as file:
                        json.dump(data, file, indent=4,)
                
            case SaveFormat.YAML:
                 with open(full_path, 'w', encoding='utf-8') as file:
                    yaml.dump(data, file, default_flow_style=False)
                #XML muss erneut angepasst werden weil das lade naktuell im spiel selbst scheitert 
            case SaveFormat.XML:
                root = ET.Element("Data") # Ein allgemeiner Oberbegriff/ Wir gehen in einer Schleife durch dein Dictionary 'data' / sucht den Platz im Garten aus und bestimmst, was für ein Baum es werden soll (die Wurzel)
                for key, value in data.items():# Wir erstellen für JEDEN Schlüssel im Dictionary ein XML-Element / lässt die Äste und Zweige wachsen. Jeder Ast bekommt ein Schildchen mit dem Wert (deine Daten)
                    if isinstance(value, list):
                        list_root = ET.SubElement(root, str(key))
                        for item in value:
                            item_el = ET.SubElement(list_root, "wert")
                            item_el.text = str(item)
                    else:
                        element = ET.SubElement(root, str(key)) #in dieser Schleife wird alles aufgeschrieben
                        element.text = str(value)
                #Ende der Schleife hier ist die Liste quasi fertig im speicher / im Anchluss wird der Baum gepflanzt    
                tree = ET.ElementTree(root)#etzt wird der Baum fest eingepflanzt. Aus den einzelnen Teilen (Wurzel und Äste) wird ein festes, zusammenhängendes Ganzes – der ElementTree.
                tree.write(full_path, encoding="utf-8", xml_declaration=True)#Das ist wie ein Foto vom Baum machen und es in dein Fotoalbum (die Festplatte) kleben, damit es für immer gespeichert bleibt.
                    
            case _:
                print(f"Format {format_type} unbekannt.")#bei falscher format eingabe erscheint diese sicherheitsausgabe damit das spiel nicht abstürzt
                return

        print(f"Speichern erfolgreich in Ordner {save_folder} : {filename_ohne_pfad}")

    except Exception as e:
        print(f"Fehler beim Speichern von {full_path}: {e}")

def load_data(full_path: str, format_type: SaveFormat) -> Any:
    """Lädt Daten basierend auf dem Format und gibt sie zurück oder None bei Fehlern."""
     #full_filename = f"{base_filename}.{format_type.value.lower()}" wurde entfernt da sie zu einer doppelendung beim daten ladn führte z.B. spiel_statistik_20260217_1158.json.json was logischer weise not found auslöste
    if not os.path.exists(full_path):
        print(f"Datei nicht gefunden: {full_path}")
        return None
    
    try:
        match format_type:
            case SaveFormat.JSON:
                with open(full_path, "r", encoding="utf-8") as file:
                    return json.load(file)
                
                
            case SaveFormat.YAML:
                with open(full_path, "r", encoding="utf-8") as file:
                    return yaml.safe_load(file)    
        #Angepasst um es universell einsetzbar zu machen / wir erschaffen ein Setzling(oder Kind) vom Baum
            case SaveFormat.XML:
                tree = ET.parse(full_path)
                root = tree.getroot()
                ergebnis_dict = {}
                # Wir gehen durch jedes Element (setzling) im Wurzel-Tag <Data>
                for setzling in root:
                # setzling.tag ist der Name (z.B. "seiten") setzling.text ist der Wert (z.B. "6")
                #da xml alles als text speichert müsse nwir Zahlen wieder in echt Zahlen verwandeln über wert.isdigit() beispiel "42".isdigit() ist True (funktioniert).
                    if len(setzling) > 0:
                        ergebnis_dict[setzling.tag] = [int(i.text) for i in setzling]
                    else:
                        # Ein einzelner Wert
                        wert = setzling.text
                        if wert and wert.isdigit():
                            wert = int(wert)
                        ergebnis_dict[setzling.tag] = wert
                return ergebnis_dict
   
    except Exception as e:
        print(f"Fehler beim Laden von {full_path}: {e}")
        return None    
    
    #wir fügen eine kleine fumktion ein die eine Liste ausgibt (dateinamen) / sie ist am Ende eingefügt das sie nicht so wichtig ist   
def get_all_savefiles(base_filename: str) -> list[str]:
    
    save_folder = "saves"
    #sicherstellen das wir nicht in einen leeren Ordner(raum) greifen
    if not os.path.exists(save_folder):
        return []
    
    all_files = os.listdir(save_folder)#hier wird der inhalt des Ordners aufgelistet
   
    #an dieser stell filtern wir nur die Namen und hängen den Pfad wider dran/Wichtig damit load_data weiß in welchen Ordener zu suchen ist/ eine ausgabe mit print ist hier unnötig 
    dateien_mit_pfad = []
    for f in all_files:
        if f.startswith(base_filename):
            voller_pfad = os.path.join(save_folder, f)
            dateien_mit_pfad.append(voller_pfad)
            
    return sorted(dateien_mit_pfad, reverse=True)
    
    
    
    
    
    