import os
import csv

class Auto():
    def __init__(self, row, col, lengte, naam, ligging):
        # Coördinaat x en y tuple
        self.positie = (row - 1, col - 1)
        self.lengte = lengte
        self.naam = naam
        # Horizontaal of verticaal
        self.ligging = ligging

class Grid():
    def __init__(self, size):
        # Maakt grid van 6x6 met _
        self.size = size
        self.grid = [['_'] * size for _ in range(size)]

    def toevoeg_auto(self, auto):
        row, col = auto.positie
        if auto.ligging == 'H':
            # Kijken of auto past op bord
            if col + auto.lengte > self.size:
                raise ValueError("Past niet op het bord!")
            # Kijken of niet overlapt
            for i in range(auto.lengte):
                if self.grid[row][col + i] != '_':
                    raise ValueError("Auto overlapt!")
            # Voeg auto toe
            for i in range(auto.lengte):
                self.grid[row][col + i] = auto.naam

        elif auto.ligging == 'V':
            # Kijken of auto past op bord
            if row + auto.lengte > self.size:
                raise ValueError("Past niet op het bord!")
            # Kijken of niet overlapt
            for j in range(auto.lengte):
                if self.grid[row + j][col] != '_':
                    raise ValueError("Auto overlapt!")
            # Voeg auto toe
            for j in range(auto.lengte):
                self.grid[row + j][col] = auto.naam

    # Kijken of bord is opgelost.
    # Lijkt op toon_bord functie.
    def opgelost(self):
        # Door elke rij bord.
        for row in self.grid:
            # Door elke cel
            for col_index, cell in enumerate(row):
                # Als Cell X is
                if cell == "X":
                    # Als X op goede plek staat
                    if col_index == self.size - 1:
                        return True
        return False


    def is_vrij(self, auto, richting, stappen):
        row, col = auto.positie
        lengte = auto.lengte
        ligging = auto.ligging

        if ligging == 'H':
            if richting == "Rechts":
                for i in range(stappen):
                    if col + lengte + i >= self.size or self.grid[row][col + lengte + i] != "_":
                        return False
                    
            elif richting =="Links":
                for i in range(stappen):
                    if col - 1 - i  < 0 or self.grid[row][col - 1 - i] != "_":
                        return False
                    
        elif ligging == 'V':
            if richting == "Onder":
                for i in range(stappen):
                    if row + lengte + i >= self.size or self.grid[row + lengte + i][col] != "_":
                        return False
                    
            elif richting == "Boven":
                for i in range(stappen):
                    if row - 1 - i < 0 or self.grid[row - 1 - i][col] != "_":
                        return False

        return True

        
    def toon_bord(self):
        # Voeg een bovenste rand toe
        print("#  " * (self.size + 2))  # Twee extra kolommen voor de border

        for row_index, row in enumerate(self.grid):
            # Voeg een linker rand toe
            row_string = "#  " + " ".join(f"{cel:<2}" for cel in row)
            # Controleer of dit de rij is waar de uitgang zit
            if any(cel == "X" for cel in row):
                # Laat de rechterkant open
                print(row_string + " ")
            else:
                # Voeg een rechter rand toe
                print(row_string + " #")

        # Voeg een onderste rand toe
        print("#  " * (self.size + 2))
        
        print('\n')

    def beweeg_auto(self, auto, richting, stapgrootte):
        row, col = auto.positie
        
        # Ligging horizontaal
        if auto.ligging == 'H':
            if richting == 'Links':
                # binnen grid en vakje links is _
                if col - stapgrootte >= 0 and all(self.grid[row][col - i] == '_' for i in range(1, stapgrootte + 1)):
                    # Naar links
                    for i in range(auto.lengte):
                        self.grid[row][col - stapgrootte + i] = auto.naam
                    # rechtse worden leeg
                    for i in range(stapgrootte):
                        self.grid[row][col + auto.lengte - i - 1] = '_'
                    # Positieverandering
                    col -= stapgrootte
                else:
                    print("Oei botsing, beweging niet mogelijk!")   
                    print('\n')

            elif richting == 'Rechts':
                if col + stapgrootte + auto.lengte - 1 < self.size and all(self.grid[row][col + auto.lengte + i] == '_' for i in range(stapgrootte)):
                    for i in range(auto.lengte):
                        self.grid[row][col + stapgrootte + i] = auto.naam
                    # Meest linkse wordt leeg
                    for i in range(stapgrootte):
                        self.grid[row][col + i] = '_'
                    # Positieverandering
                    col += stapgrootte
                else:
                    print("Oei botsing, beweging niet mogelijk!") 
                    print('\n')

        # Ligging verticaal
        elif auto.ligging == 'V':
            if richting == 'Boven':
                if row - stapgrootte >= 0 and all(self.grid[row - i][col] == '_' for i in range(1, stapgrootte + 1)):
                    for i in range(auto.lengte):
                        self.grid[row - stapgrootte + i][col] = auto.naam
                    for i in range(stapgrootte):
                        self.grid[row + auto.lengte - i - 1][col] = '_'
                    row -= stapgrootte
                else:
                    print("Oei botsing, beweging niet mogelijk!")
                    print('\n')
            
            elif richting == 'Onder':
                if row + stapgrootte + auto.lengte - 1 < self.size and all(self.grid[row + auto.lengte + i][col] == '_' for i in range(stapgrootte)):
                    for i in range(auto.lengte):
                        self.grid[row + stapgrootte + i][col] = auto.naam
                    for i in range(stapgrootte):
                        self.grid[row + i][col] = '_'
                    row += stapgrootte
                else:
                    print("Oei botsing of buiten het speelveld, beweging niet mogelijk!")
                    print('\n')
            else:
                raise ValueError("Ongeldige richting voor verticale auto!")
        # Update positie
        auto.positie = (row, col)
        
        
        
def lees_csv_bestand(pad):
    autos = []
    with open(pad, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Sla de kopregel over
        for row in reader:
            naam = row[0]  # ID van de auto
            ligging = row[1]  # 'H' of 'V'
            col = int(row[2])
            rij = int(row[3])
            lengte = int(row[4])
            autos.append(Auto(rij, col, lengte, naam, ligging))
    return autos

def kies_spelbord(mapnaam):
    bestanden = [f for f in os.listdir(mapnaam) if f.startswith("Rushhour") and f.endswith(".csv")]
    if not bestanden:
        print("Geen spelborden gevonden in de map.")
        return None

    spellen = []
    for bestand in bestanden:
        # Splits de bestandsnaam op de underscore en haal de size en het nummer eruit
        naam_deel = bestand.split('_')
        if len(naam_deel) >= 2:
            try:
                # Verkrijg de size en spelnummer
                size_deel = naam_deel[0].replace('Rushhour', '')  # Haal "Rushhour" weg
                
                # Controleer of de grootte uit één of twee cijfers bestaat
                if len(size_deel) >= 2 and size_deel[1].isdigit():
                    size = int(size_deel[:2])  # Neem de eerste twee karakters als getal (bijv. '12' uit '12x12')
                else:
                    size = int(size_deel[0])  # Neem het eerste cijfer (bijv. '6' uit '6x6')
                
                # Haal het spelnummer eruit
                spelnummer = int(naam_deel[1].replace('.csv', ''))
                
                # Voeg het spel toe aan de lijst
                spellen.append((spelnummer, size, bestand))
            except ValueError:
                continue  # Als de waarde geen nummer is, sla deze over


    # Sorteer de spellen op spelnummer
    spellen.sort()  # Sorteert eerst op spelnummer, dus van klein naar groot

    while True:
        try:
            keuze = int(input(f"Kies een spelbord (1-{len(spellen)}): "))
            if 1 <= keuze <= len(spellen):
                gekozen_bestand = spellen[keuze - 1][2]
                size = spellen[keuze - 1][1]
                return os.path.join(mapnaam, gekozen_bestand), size
            else:
                print("Ongeldige keuze, probeer opnieuw.")
        except ValueError:
            print("Voer een geldig nummer in.")

# Voorbeeldgebruik
def vraag_en_beweeg(speelveld, autos):
    """
    Vraag de gebruiker om een auto te verplaatsen en voer de beweging uit.
    """
    while True:
        try:
            # Vraag om de naam van de auto
            auto_naam = input("Welke auto wil je verplaatsen? ").strip()
            auto_naam = auto_naam.upper()
            # Controleer of de auto bestaat
            auto = next((a for a in autos if a.naam == auto_naam), None)
            if not auto:
                print("Auto niet gevonden. Probeer opnieuw.")
                continue

            # Vraag om het aantal blokjes om te verplaatsen
            stappen = int(input("Met hoeveel blokjes wil je de auto verplaatsen? (Bijvoorbeeld: -2 voor achteruit, 3 voor vooruit): "))
            
            # Bepaal de richting op basis van de ligging van de auto
            if stappen > 0 and auto.ligging == "H":
                richting = "Rechts"
            elif stappen < 0 and auto.ligging == "H":
                richting = "Links"
            elif stappen > 0 and auto.ligging == "V":
                richting = "Onder"
            elif stappen < 0 and auto.ligging == "V":
                richting = "Boven"

            # Roep jouw beweeg_auto functie aan
            speelveld.beweeg_auto(auto, richting, abs(stappen))
            
            # Beweging succesvol, stop de loop
            break
        except ValueError:
            print("Ongeldige invoer")

# Game loop voorbeeld
if __name__ == "__main__":
    mapnaam = "gameboards"  # Map waar spelborden staan
    pad_naar_csv, size = kies_spelbord(mapnaam)
    if pad_naar_csv:
        autos = lees_csv_bestand(pad_naar_csv)

        speelveld = Grid(size)
        for auto in autos:
            speelveld.toevoeg_auto(auto)

        while True:
            speelveld.toon_bord()
            vraag_en_beweeg(speelveld, autos)

            # Controleer of de X aan de rechterkant is om het spel te winnen
            if any(auto.naam == "X" and auto.positie[1] + auto.lengte - 1 == size - 1 for auto in autos):
                speelveld.toon_bord()
                print("Gefeliciteerd! Je hebt het spel gewonnen!")
                break
