import os
import time
import random
import json 
import sqlite3
from domain.wuerfel import Wuerfel
from application.rangliste_service import erstelle_rangliste
from application.wuerfelspiel_service import sichere_spielstand
import application.wuerfelspiel_service as service
from infrastructure.ansii_asset import DICE_ART, POKAL
from interface.ui_helpers import display_welcome_message, display_loading_screen
from infrastructure.style_config import FETT, GOLD, GELB, RESET, CYAN, GRUEN, SILBER, BRONZE, ROT
from infrastructure.sqlite_repository import SQLiteRepository

# ... restlicher Code
def animiere_wurf():
    # Wir zeigen 10 zufällige Würfelbilder hintereinander
    for i in range(12):
        # 1. Bildschirm leeren (WICHTIG für Animation)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # 2. Zufällige Zahl für die Animation wählen
        dummy_zahl = random.randint(1, 6)
        print(f"{GELB}Der Würfel rollt...{RESET}")
        print_dice(dummy_zahl)
        
        # 3. Kurz warten (am Anfang schnell, am Ende langsamer für Realismus)
        time.sleep(0.05 + (i * 0.02))

def print_dice(zahl): # Zahl ist die Augenzahl, die gewürfelt wurde 
    if zahl in DICE_ART:# Überprüfen, ob die Augenzahl eine gültige Darstellung im DICE_ART-Dictionary hat
        for zeile in DICE_ART[zahl]:# Iterieren über die Zeilen der ASCII-Art für die gewürfelte Zahl und Ausgabe jeder Zeile mit der gewünschten Farbe (CYAN) und anschließendem Reset der Farbe
            print(f"{CYAN}{zeile}{RESET}")# Wenn die Augenzahl nicht im DICE_ART-Dictionary vorhanden ist, wird eine Fehlermeldung ausgegeben

def spielstand_laden():
    conn = sqlite3.connect("wuerfel_save.db")
    cursor = conn.cursor()
    
    # 1. Wir holen die Daten mit, um die Namen zu extrahieren
    cursor.execute("SELECT id, typ, timestamp, daten FROM spielstaende ORDER BY id DESC")
    speicherungen = cursor.fetchall()
    conn.close()
    
    print("\n--- Verfügbare Spielstände ---")
    if not speicherungen:
        print("Keine Spielstände gefunden.")
    else:
        for i, (db_id, typ, ts, daten_json) in enumerate(speicherungen, start=1): # Iterieren über die gefundenen Spielstände, wobei "i" die fortlaufende Nummer der Anzeige ist, "db_id" die ID des Spielstands in der Datenbank, "typ" der Typ des Spielstands (z.B. "AUTOSAVE"), "ts" der Timestamp der Speicherung und "daten_json" die gespeicherten Spieldaten im JSON-Format sind. Für jeden Spielstand werden die Daten aus dem JSON-String geladen, die Namen der Spieler*innen extrahiert und eine übersichtliche Anzeige mit der Nummer, dem Timestamp, dem Typ und den Spielernamen erstellt.
            data = json.loads(daten_json) # Laden der gespeicherten Spieldaten aus dem JSON-String, um Zugriff auf die Informationen zu erhalten, die für die Anzeige benötigt werden (z.B. die Namen der Spieler
            spieler_namen = ", ".join([s["name"] for s in data["mehrspieler_daten"]]) # Extrahieren der Namen der Spieler*innen aus den geladenen Spieldaten, indem über die Liste "mehrspieler_daten" iteriert und die Namen der Spieler
            
            print(f"{CYAN}{i}: {RESET}[{ts}] {FETT}{typ}{RESET}") # Anzeige der Nummer, des Timestamps und des Typs des Spielstands in einer übersichtlichen Formatierung, wobei die Nummer in Cyan, der Typ fett und der Timestamp normal formatiert ist. Anschließend werden die Namen der Spieler*innen angezeigt, um dem Benutzer eine klare Vorstellung davon zu geben, welcher Spielstand geladen wird.
            print(f"   {GELB}↳ Spieler: {RESET}{spieler_namen}") # Anzeige der Namen der Spieler*innen, die in dem jeweiligen Spielstand enthalten sind, um dem Benutzer zusätzliche Informationen zu geben und die Auswahl des gewünschten Spielstands zu erleichtern. Die Namen werden in Gelb formatiert, um sie hervorzuheben und die Aufmerksamkeit des Benutzers darauf zu lenken.
            print("-" * 30) # Trennlinie zwischen den Einträgen für eine bessere Lesbarkeit
        
    
    print("-" * 30)
    print(f"{GRUEN}0: Neues Spiel starten{RESET}")
    print(f"{ROT}9: Datenbank komplett leeren (VORSICHT!){RESET}")
    
    wahl = input("\nAuswahl: ").strip()
    
    # --- LOGIK FÜR AKTIONEN ---
    if wahl == "9":
        bestaetigung = input("Wirklich alle Spielstände unwiderruflich löschen? (j/n): ").lower()
        if bestaetigung == "j":
            repo = SQLiteRepository("wuerfel_save.db")
            repo.leere_datenbank()
        return None # Zurück zum Start/Neues Spiel
        
    if wahl == "0" or wahl == "": 
        return None
   
    try:
        index = int(wahl) - 1
        # Prüfen, ob die Nummer existiert
        if index < 0 or index >= len(speicherungen):
            print("❌ Ungültige Auswahl.")
            return None
            
        gewaehlte_id = speicherungen[index][0]
        
        # 2. Den gewählten Spielstand aus der DB holen
        conn = sqlite3.connect("wuerfel_save.db")
        cursor = conn.cursor()
        cursor.execute("SELECT daten FROM spielstaende WHERE id = ?", (gewaehlte_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            info_raw = json.loads(row[0])
            
            # 3. Daten in die Würfel-Objekte umwandeln
            geladene_wuerfel = []
            for s_info in info_raw["mehrspieler_daten"]:
                w = Wuerfel(name=s_info["name"], start_statistik=s_info["statistik"])
                geladene_wuerfel.append(w)
            
            return {
                "wuerfel_liste": geladene_wuerfel,
                "max_wuerfe": info_raw.get("max_wuerfe", 30),
                "start_index": info_raw.get("naechster_spieler_index", 0)
            }
            
    except Exception as e:
        print(f"❌ Fehler beim Laden aus der Datenbank: {e}")
    return None

def wuerfel_spiel(): # Hauptfunktion, die den Ablauf des Würfelspiels steuert. Sie ermöglicht das Laden eines bestehenden Spielstands oder das Starten eines neuen Spiels, verwaltet die Spielrunden und zeigt am Ende die Siegerehrung an.
    display_loading_screen() # Aufruf der Funktion display_loading_screen, um eine Ladeanimation anzuzeigen, bevor das Spiel beginnt. Dies verbessert die Benutzererfahrung, indem es den Eindruck vermittelt, dass das System vorbereitet wird, und schafft eine ansprechende Atmosphäre für den Start des Spiels.
    display_welcome_message()
    info = spielstand_laden() # Aufruf der Funktion spielstand_laden, um zu versuchen, einen bestehenden Spielstand zu laden. Das Ergebnis wird in der Variable "info" gespeichert, die entweder ein Dictionary mit den geladenen Daten oder None enthält, wenn kein Spielstand geladen wurde.
    
    if info: # Wenn ein Spielstand erfolgreich geladen wurde (d.h. "info" ist nicht None), werden die geladenen Daten extrahiert, um die Liste der Würfel-Objekte, die maximalen Würfe und den Startindex zu erhalten. Anschließend wird eine Bestätigung ausgegeben, dass der Spielstand geladen wurde, und das Spiel kann mit den geladenen Daten fortgesetzt werden.
        alle_wuerfel = info["wuerfel_liste"]
        max_wuerfe = info["max_wuerfe"]
        start_index = info["start_index"]
        print(f"✅ Geladen! Weiter geht's mit {alle_wuerfel[start_index].name}.")
    else:
        while True:
            anz_in = input("Wie viele Spieler*innen (1-10)? ").strip() # Eingabeaufforderung für die Anzahl der Spieler*innen, die am Spiel teilnehmen sollen. Die Eingabe wird bereinigt (strip), um unerwünschte Leerzeichen zu entfernen. Es wird erwartet, dass die Eingabe eine Zahl zwischen 1 und 10 ist.
            if anz_in.isdigit() and 1 <= int(anz_in) <= 10: # Überprüfung, ob die Eingabe eine gültige Zahl ist und ob sie im Bereich von 1 bis 10 liegt. Wenn die Eingabe gültig ist, wird sie in eine Ganzzahl umgewandelt und in der Variable "anzahl" gespeichert. Anschließend wird die Schleife verlassen, um mit der Erstellung der Spieler fortzufahren.
                anzahl = int(anz_in) # Umwandlung der gültigen Eingabe in eine Ganzzahl, die die Anzahl der Spieler*innen repräsentiert. Diese Zahl wird später verwendet, um die entsprechende Anzahl von Würfel-Objekten zu erstellen und die Spieler*innen zu benennen.
                break
            print("❌ Ungültig (1-10)!")

        alle_wuerfel = [] # Leere Liste, um die Würfel-Objekte der Spieler*innen zu speichern. Diese Liste wird später mit den erstellten Würfel-Objekten gefüllt, die die Namen und Statistiken der Spieler*innen enthalten.
        for i in range(anzahl): # Schleife, die von 0 bis zur Anzahl der Spieler*innen läuft, um für jeden Spieler*in ein Würfel-Objekt zu erstellen. In jeder Iteration wird der Benutzer aufgefordert, einen Namen für den Spieler*in einzugeben, und es wird überprüft, ob der Name nur aus Buchstaben besteht. Wenn der Name gültig ist, wird ein neues Würfel-Objekt mit diesem Namen erstellt und zur Liste "alle_wuerfel" hinzugefügt. Wenn der Name ungültig ist, wird eine Fehlermeldung ausgegeben und die Eingabeaufforderung wiederholt, bis ein gültiger Name eingegeben wird.
            while True:
                name = input(f"Name für Spieler*in {i+1}: ").strip() # Eingabeaufforderung für den Namen des Spieler*in, der in der aktuellen Iteration erstellt wird. Die Eingabe wird bereinigt (strip), um unerwünschte Leerzeichen zu entfernen. Es wird erwartet, dass der Name nur aus Buchstaben besteht.
                if name.isalpha(): # Überprüfung, ob der eingegebene Name nur aus Buchstaben besteht. Wenn die Eingabe gültig ist, wird ein neues Würfel-Objekt mit diesem Namen erstellt und zur Liste "alle_wuerfel" hinzugefügt. Anschließend wird die Schleife verlassen, um mit der nächsten Iteration fortzufahren. Wenn die Eingabe ungültig ist, wird eine Fehlermeldung ausgegeben und die Eingabeaufforderung wiederholt, bis ein gültiger Name eingegeben wird.
                    alle_wuerfel.append(Wuerfel(name=name)) # Erstellung eines neuen Würfel-Objekts mit dem gültigen Namen und Hinzufügen dieses Objekts zur Liste "alle_wuerfel", die alle Spieler*innen repräsentiert. Jedes Würfel-Objekt enthält den Namen des Spieler*in und eine Statistik, die im Laufe des Spiels aktualisiert wird.
                    break
                print("❌ Nur Buchstaben!")

        while True:
            r_in = input("Wie viele Würfe pro Spieler? ").strip() # Eingabeaufforderung für die Anzahl der Würfe, die jeder Spieler*in pro Spielrunde haben soll. Die Eingabe wird bereinigt (strip), um unerwünschte Leerzeichen zu entfernen. Es wird erwartet, dass die Eingabe eine positive Zahl ist, die angibt, wie viele Würfe jeder Spieler*in in einer Runde durchführen darf.
            if r_in.isdigit() and int(r_in) > 0: # Überprüfung, ob die Eingabe eine gültige Zahl ist und ob sie größer als 0 ist. Wenn die Eingabe gültig ist, wird sie in eine Ganzzahl umgewandelt und in der Variable "max_wuerfe" gespeichert, die die maximale Anzahl der Würfe pro Spieler*in repräsentiert. Anschließend wird die Schleife verlassen, um mit dem Spiel fortzufahren. Wenn die Eingabe ungültig ist, wird eine Fehlermeldung ausgegeben und die Eingabeaufforderung wiederholt, bis eine gültige Zahl eingegeben wird.
                max_wuerfe = int(r_in) # Umwandlung der gültigen Eingabe in eine Ganzzahl, die die maximale Anzahl der Würfe pro Spieler*in repräsentiert. Diese Zahl wird später verwendet, um zu überprüfen, ob ein Spieler*in seine maximale Anzahl an Würfen erreicht hat und um das Spiel entsprechend zu steuern.
                break
            print("❌ Bitte Zahl > 0!")
        
        start_index = 0 # Variable, die den Index des nächsten Spieler*in speichert, der am Zug ist. Sie wird verwendet, um den Spielablauf zu steuern und sicherzustellen, dass die Spieler*innen in der richtigen Reihenfolge spielen. Zu Beginn des Spiels wird sie auf 0 gesetzt, was bedeutet, dass der erste Spieler*in in der Liste "alle_wuerfel" am Zug ist.

    spiel_aktiv = True # Variable, die den Status des Spiels repräsentiert. Sie wird verwendet, um die Hauptspielschleife zu steuern. Solange "spiel_aktiv" True ist, läuft das Spiel weiter. Wenn das Spiel endet (z.B. wenn alle Spieler*innen ihre maximale Anzahl an Würfen erreicht haben oder wenn der Benutzer das Spiel manuell speichert und verlässt), wird "spiel_aktiv" auf False gesetzt, um die Schleife zu beenden und das Spiel zu beenden.
    while spiel_aktiv: # Hauptspielschleife, die so lange läuft, wie "spiel_aktiv" True ist. In dieser Schleife wird der Spielablauf gesteuert, einschließlich der Anzeige der aktuellen Rangliste, der Durchführung der Spielzüge für jeden Spieler*in und der Überprüfung, ob das Spiel beendet werden soll (z.B. wenn alle Spieler*innen ihre maximale Anzahl an Würfen erreicht haben). Am Ende jeder Runde wird der Spielstand gesichert, um sicherzustellen, dass der Fortsch
        
        runde = min(w.get_gesamtanzahl() for w in alle_wuerfel) + 1
        
        # Falls die Runde das Maximum überschreitet (am Ende des Spiels), begrenzen wir sie
        if runde > max_wuerfe:
            runde = max_wuerfe

        service.zeige_runden_header(runde, max_wuerfe)
        service.zeige_rangliste(alle_wuerfel)

        for i in range(start_index, len(alle_wuerfel)): # Schleife, die von "start_index" bis zur Anzahl der Spieler*innen läuft, um den Spielzug für jeden Spieler*in in der aktuellen Runde durchzuführen. In jeder Iteration wird überprüft, ob der aktuelle Spieler*in seine maximale Anzahl an Würfen erreicht hat. Wenn ja, wird dieser Spieler*in übersprungen. Andernfalls wird der Spieler*in aufgefordert, eine Entscheidung zu treffen (Rollen, Statistik anzeigen oder Spiel speichern). Je nach Entscheidung wird der entsprechende Spielzug durchgeführt (z.B. Würfeln, Statistik anzeigen oder Spiel speichern). Am Ende der Runde wird der "start_index" zurückgesetzt und der Spielstand gesichert.
            mein_wuerfel = alle_wuerfel[i] # Abrufen des Würfel-Objekts für den aktuellen Spieler*in basierend auf dem Index "i". Dieses Objekt enthält den Namen und die Statistik des Spieler*in, die im Laufe des Spiels aktualisiert werden.
            if mein_wuerfel.get_gesamtanzahl() >= max_wuerfe: # Überprüfung, ob der aktuelle Spieler*in seine maximale Anzahl an Würfen erreicht hat. Wenn dies der Fall ist, wird eine Nachricht ausgegeben, dass der Spieler*in übersprungen wird, und die Schleife fährt mit dem nächsten Spieler*in fort. Dies stellt sicher, dass Spieler*innen, die bereits ihre maximale Anzahl an Würfen erreicht haben, nicht mehr am Spiel teilnehmen können und das Spiel entsprechend gesteuert wird.
                continue
            
            wurf_nummer = mein_wuerfel.get_gesamtanzahl() + 1 # Berechnung der aktuellen Wurfnummer für den Spieler*in, indem die Gesamtanzahl der bisherigen Würfe um 1 erhöht wird. Diese Wurfnummer wird verwendet, um dem Spieler*in anzuzeigen, wie viele Würfe er/sie bereits in der aktuellen Runde gemacht hat und wie viele Würfe noch übrig sind, basierend auf der maximalen Anzahl der Würfe pro Spieler*in.
            print(f"\n{FETT}>>> {mein_wuerfel.name} ist am Zug (Wurf {wurf_nummer}/{max_wuerfe}) <<<{RESET}") # Anzeige, welcher Spieler*in am Zug ist und wie viele Würfe er/sie bereits in der aktuellen Runde gemacht hat. Es wird der Name des Spieler*in und die aktuelle Wurfnummer im Verhältnis zur maximalen Anzahl der Würfe angezeigt, um dem Spieler*in eine klare Vorstellung davon zu geben, wie viele Würfe er/sie noch in dieser Runde hat.
            
            entscheidung = input("Rollen (Enter), Statistik (s), Speichern (q): ").lower().strip()

            if entscheidung == "s":
                print(f"Statistik: {mein_wuerfel.statistik}")
                input("Weiter mit Enter...")
            elif entscheidung == "q":
                sichere_spielstand(alle_wuerfel, max_wuerfe, i, "manueller_save")
                spiel_aktiv = False
                break
            
            if not entscheidung:
                animiere_wurf()
                ergebnis = mein_wuerfel.rollen()
                print_dice(ergebnis)
                print(f"🎲 {GRUEN}{mein_wuerfel.name}{RESET} würfelt eine {FETT}{ergebnis}{RESET}!")
                # Ausskommentiert da nutzen fragwürdig und Perfomance-Problem durch ständiges Speichern und unnötiges voll laufen der DB 
                #naechster_spieler = (i + 1) % len(alle_wuerfel) # Berechnung des Index des nächsten Spieler*in, der am Zug sein wird, indem der aktuelle Index "i" um 1 erhöht und dann modulo der Anzahl der Spieler*innen genommen wird. Dies stellt sicher, dass der Index wieder bei 0 beginnt, wenn das Ende der Liste erreicht ist, und ermöglicht einen kontinuierlichen Spielablauf, bei dem die Spieler*innen in der richtigen Reihenfolge spielen.
                #sichere_spielstand(alle_wuerfel, max_wuerfe, naechster_spieler, "wurf_save")
                #print(f"{CYAN}Info: Spielstand wurde nach diesem Wurf gesichert.{RESET}")

        if not spiel_aktiv: 
            break

        # Runde beendet, Index zurücksetzen für nächste Runde
        start_index = 0 
        sichere_spielstand(alle_wuerfel, max_wuerfe, 0, "runden_backup") # Nach jeder Runde wird der Spielstand automatisch gesichert, um sicherzustellen, dass der Fortschritt nicht verloren geht. Es wird ein Backup mit dem Typ "runden_backup" erstellt, das die aktuellen Daten aller Spieler*innen, die maximale Anzahl der Würfe und den Startindex für die nächste Runde enthält. Dieses Backup kann später verwendet werden, um den Spielstand wiederherzustellen, falls das Spiel unerwartet unterbrochen wird oder wenn der Benutzer das Spiel manuell speichert und verlässt.

        # Check: Sind alle fertig? -> Siegerehrung
        if all(w.get_gesamtanzahl() >= max_wuerfe for w in alle_wuerfel): # Überprüfung, ob alle Spieler*innen ihre maximale Anzahl an Würfen erreicht haben. Wenn dies der Fall ist, bedeutet dies, dass das Spiel beendet ist und die Siegerehrung durchgeführt werden kann. In diesem Fall wird die Variable "spiel_aktiv" auf False gesetzt, um die Hauptspielschleife zu beenden und zur Siegerehrung überzugehen.
            
            print("\n\n" + "="*45)
            print(f"{GOLD}{FETT}      🏆 DIE GROSSE SIEGEREHRUNG 🏆{RESET}")
            print("="*45)
            time.sleep(1) 
            
            # Den Pokal anzeigen
            for zeile in POKAL: # Iteration über die Zeilen der ASCII-Art des Pokals, um ihn in der Konsole anzuzeigen. Jede Zeile wird zentriert und mit der Farbe GOLD und dem Format FETT ausgegeben, um die Siegerehrung visuell ansprechend zu gestalten. Nach der Ausgabe jeder Zeile wird eine kurze Pause von 0,7 Sekunden eingelegt, um die Spannung zu erhöhen und die Aufmerksamkeit auf die Siegerehrung zu lenken.
                print(f"{GOLD}{zeile.center(45)}{RESET}") # Ausgabe der Zeile der ASCII-Art des Pokals, zentriert und mit der Farbe GOLD und dem Format FETT, um die Siegerehrung visuell ansprechend zu gestalten. Nach der Ausgabe jeder Zeile wird eine kurze Pause von 0,7 Sekunden eingelegt, um die Spannung zu erhöhen und die Aufmerksamkeit auf die Siegerehrung zu lenken.
            print("\n")
            
            end_rangliste = erstelle_rangliste(alle_wuerfel)
            letzte_punktzahl = -1
            aktueller_platz = 0

            for i, (name, punkte) in enumerate(end_rangliste): # Iteration über die endgültige Rangliste, um die Platzierungen der Spieler*innen anzuzeigen. In jeder Iteration wird überprüft, ob die Punktzahl des aktuellen Spieler*in ungleich der letzten Punktzahl ist. Wenn dies der Fall ist, wird der aktuelle Platz erhöht (da es sich um eine neue Punktzahl handelt). Wenn die Punktzahl gleich der letzten Punktzahl ist, bleibt der aktuelle Platz gleich (was bedeutet, dass es sich um einen geteilten Rang handelt). Anschließend wird basierend auf dem aktuellen Platz eine entsprechende Medaille (Gold für Platz 1, Silber für Platz 2, Bronze für Platz 3) und die Farbe festgelegt. Schließlich wird die Platzierung des Spieler*in mit seinem Namen und seiner Punktzahl in der entsprechenden Farbe und Formatierung ausgegeben.
                # Wenn die Punkte ungleich dem Vorgänger sind, erhöht sich der Platz
                # Wenn sie gleich sind, bleibt der Platz gleich (geteilter Rang)
                if punkte != letzte_punktzahl: # Überprüfung, ob die Punktzahl des aktuellen Spieler*in ungleich der letzten Punktzahl ist. Wenn dies der Fall ist, bedeutet dies, dass es sich um eine neue Punktzahl handelt und der aktuelle Platz erhöht werden muss. Wenn die Punktzahl gleich der letzten Punktzahl ist, bleibt der aktuelle Platz gleich, was darauf hinweist, dass es sich um einen geteilten Rang handelt.
                    aktueller_platz = i + 1
                
                letzte_punktzahl = punkte
                
                prefix = ""
                farbe = RESET
                
                # Jetzt nutzen wir 'aktueller_platz' für die Medaillen-Logik und die Farbauswahl
                if aktueller_platz == 1:
                    prefix = "🥇 "; farbe = GOLD + FETT
                elif aktueller_platz == 2:
                    prefix = "🥈 "; farbe = SILBER
                elif aktueller_platz == 3:
                    prefix = "🥉 "; farbe = BRONZE
                else:
                    prefix = "   "
                
                time.sleep(0.7)
                print(f"{farbe}{prefix}Platz {aktueller_platz}: {name:<12} | {punkte:>3} Punkte{RESET}")
            
            winner_name = end_rangliste[0][0]
            print("\n" + "="*45)
            print(f"{GRUEN}{FETT}Herzlichen Glückwunsch, {winner_name}!{RESET}")
            print(f"{GRUEN}Du hast das Turnier dominiert!{RESET}")
            print("="*45)
            
            spiel_aktiv = False

if __name__ == "__main__":
    wuerfel_spiel()