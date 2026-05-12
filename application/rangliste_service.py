def berechne_punkte(wuerfel_objekt): # wuerfel_objekt ist eine Instanz der Klasse Wuerfel
    return sum((i + 1) * menge for i, menge in enumerate(wuerfel_objekt.statistik))# Berechnung der Punkte basierend auf der Statistik des Würfel-Objekts, wobei jede Augenzahl mit ihrer Häufigkeit multipliziert wird und die Ergebnisse summiert werden

def bubble_sort_absteigend(liste):# liste ist eine Liste von Tupeln (Name, Punkte)
    n = len(liste)# Anzahl der Elemente in der Liste
    for i in range(n):# Äußere Schleife für die Anzahl der Durchgänge
        for j in range(0, n - i - 1):# Innere Schleife für den Vergleich der Elemente
            if liste[j][1] < liste[j + 1][1]:# Vergleich der Punkte (Index 1 im Tupel)
                liste[j], liste[j + 1] = liste[j + 1], liste[j]# Tauschen der Elemente, wenn das aktuelle Element weniger Punkte hat als das nächste
    return liste# Rückgabe der sortierten Liste in absteigender Reihenfolge

def erstelle_rangliste(alle_wuerfel):# alle_wuerfel ist eine Liste von Instanzen der Klasse Wuerfel
    daten = [] # Leere Liste, um die Namen und Punkte der Spieler zu speichern
    for w in alle_wuerfel:# Iteration über alle Würfel-Objekte in der Liste
        punkte = berechne_punkte(w)# Berechnung der Punkte für das aktuelle Würfel-Objekt
        daten.append((w.name, punkte))# Hinzufügen eines Tupels (Name, Punkte) zur Datenliste
    
    return bubble_sort_absteigend(daten)# Sortieren der Datenliste in absteigender Reihenfolge basierend auf den Punkten und Rückgabe der sortierten Liste