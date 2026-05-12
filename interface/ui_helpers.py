import time# Das time-Modul wird für die Verzögerung in der Würfel-Animation benötigt
import sys# Für die Würfel-Animation benötigen wir die time- und sys-Module
import random
from rich.console import Console
from rich.panel import Panel

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
    welcome_text = r"""                                           
 __        ___ _ _ _                                        
 \ \      / (_) | | | _____  _ __ ___  _ __ ___   ___ _ __  
  \ \ /\ / /| | | | |/ / _ \| '_ ` _ \| '_ ` _ \ / _ \ '_ \ 
   \ V  V / | | | |   < (_) | | | | | | | | | | |  __/ | | |
    \_/\_/  |_|_|_|_|\_\___/|_| |_| |_|_| |_| |_|\___|_| |_|
                                                            
    """
    console.print(Panel(welcome_text, style="bold cyan", title="Würfelspiel v1.0"))
    console.print("[yellow]Willkommen, mutiger Spieler! Bereit für eine Runde?[/yellow]\n")    

