# Wir nutzen Triple-Quotes (''' '''), um mehrzeiligen Text einfach zu speichern
# In diesem Fall speichern wir die ASCII-Art für einen Würfel, den wir später ausgeben können
DICE_ART = {
    1: (
        "┌─────────┐",
        "│         │",
        "│    ●    │",
        "│         │",
        "└─────────┘"
    ),
    2: (
        "┌─────────┐",
        "│  ●      │",
        "│         │",
        "│      ●  │",
        "└─────────┘"
    ),
    3: (
        "┌─────────┐",
        "│  ●      │",
        "│    ●    │",
        "│      ●  │",
        "└─────────┘"
    ),4: (
        "┌─────────┐",
        "│  ●   ●  │",
        "│         │",
        "│  ●   ●  │",
        "└─────────┘"
    ),5: (
        "┌─────────┐",
        "│  ●   ●  │",
        "│    ●    │",
        "│  ●   ●  │",
        "└─────────┘"
    ),6: (
        "┌─────────┐",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "│  ●   ●  │",
        "└─────────┘"
    )
    
} # Ein Dictionary, das die ASCII-Art für die Zahlen 1-6 auf einem Würfel enthält. Jede Zahl ist mit einem Tupel von Strings verbunden, die die Zeilen der ASCII-Art darstellen.
POKAL = (
    "      ___________      ",
    "     '._==_==_=_.'     ",
    "     .-\\:      /-.    ",
    "    | (|:.     |) |    ",
    "     '-|:.     |-'     ",
    "       \\::.    /      ",
    "        '::. .'        ",
    "          ) (          ",
    "        _.' '._        ",
    "       `-------`       "
) # Ein Tupel von Strings, das die ASCII-Art eines Pokals darstellt. Jede Zeile des Pokals ist ein Element im Tupel.