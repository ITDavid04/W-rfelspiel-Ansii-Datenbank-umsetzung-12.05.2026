import time# Das time-Modul wird für die Verzögerung in der Würfel-Animation benötigt
import sys# Für die Würfel-Animation benötigen wir die time- und sys-Module
import random
from rich.console import Console
from rich.panel import Panel
from infrastructure.style_config import GOLD, CYAN, GELB, GRUEN, FETT, RESET, spinner # Importieren von Stil-Konfigurationen und einem Spinner für die Ladeanimation. Diese werden verwendet, um die visuelle Gestaltung der Ladeanimation zu verbessern und den Benutzer über den Fortschritt des Ladevorgangs zu informieren. Durch die Verwendung von Farben und Formatierungen können wir die Aufmerksamkeit des Benutzers auf die Ladeanimation lenken und ein ansprechendes visuelles Erlebnis schaffen. Der Spinner wird verwendet, um eine sich drehende Animation zu erzeugen, die den Eindruck vermittelt, dass das System aktiv arbeitet und lädt.
console = Console()



def wuerfel_animation():# Diese Funktion zeigt eine einfache Würfel-Animation im Terminal
    # Die verschiedenen "Gesichter" eines Würfels
    frames = [
        "⚀", "⚁", "⚂", "⚃", "⚄", "⚅"
    ] # Unicode-Zeichen für die Würfelseiten 1-6
    
    print("Würfel rollt: ", end="", flush=True)# Start der Animation, ohne Zeilenumbruch und mit sofortigem Flush
    
    # Wir lassen 10-mal ein zufälliges Gesicht aufblitzen
    for _ in range(10):
        face = random.choice(frames)# Zufälliges Gesicht auswählen
        sys.stdout.write(f"\rWürfel rollt: {face} ") # \r springt zum Zeilenanfang
        sys.stdout.flush()
        time.sleep(0.1) # 100ms warten
    
    print() # Neue Zeile nach der Animation
    
    
def display_welcome_message():
    welcome_text = rf"""{GOLD}
╔══════════════════════════════════════════════════════════════════════════════════╗                                           
║ __        ___ _ _ _                                                   .-------.  ║
║ \ \      / (_) | | | _____  _ __ ___  _ __ ___   ___ _ __        .-------.  * |  ║
║  \ \ /\ / /| | | | |/ / _ \| '_ ` _ \| '_ ` _ \ / _ \ '_ \       | *   * | *  |  ║
║   \ V  V / | | | |   < (_) | | | | | | | | | | |  __/ | | |      |   *   |*   |  ║
║    \_/\_/  |_|_|_|_|\_\___/|_| |_| |_|_| |_| |_|\___|_| |_|      | *   * |____'  ║
║                                                                  ._______.       ║
╚══════════════════════════════════════════════════════════════════════════════════╝ 
{RESET}"""
    
    console.print(Panel(welcome_text, style="bold yellow", title="Würfelspiel v1.0"))
    print(f"{GOLD}Willkommen zum Würfelabenteur! Bereit für eine Runde?{RESET}\n")

def display_loading_screen(dauer=5):
    """Simuliert den Ladevorgang aus Code 1"""
    end_time = time.time() + dauer
    
    while time.time() < end_time:
        for char in spinner:
            # '\r' überschreibt die aktuelle Zeile
            sys.stdout.write(f"\r{GELB}Lade System... {char}{RESET}")
            sys.stdout.flush()
            time.sleep(0.1)
    
    # Abschlussmeldung
    print(f"\r{GRUEN}{FETT}System erfolgreich geladen! ✓ {RESET}   ")      
    
    
    