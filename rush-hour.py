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
    '''
    Variabele size (voor grid) toevoegen.
    '''
    def __init__(self, size):
        # Maakt grid van 6x6 met _
        self.size = size
        self.grid = [['_'] * size for _ in range(size)]
        
        '''
        Auto's toevoegen uit een csv file
        '''
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
        
    def toon_bord(self):
        for row in self.grid:
            print(' '.join(row))
    
        '''
        Finish maken
        '''
                
    '''
    Variabele 'stappen' toevoegen voor hoeveel stappen je wilt zetten met auto
    '''
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
                    
            elif richting == 'Rechts':
                if col + stappgrootte + auto.lengte - 1 < self.size and all(self.grid[row][col + auto.lengte + i] == '_' for i in range(stapgrootte)):
                    for i in range(auto.lengte):
                        self.grid[row][col + stapgrootte + i] = auto.naam
                    # Meest linkse wordt leeg
                    for i in range(stapgrootte):
                        self.grid[row][col + i] = '_'
                    # Positieverandering
                    col += stapgrootte
            else:
                raise ValueError("Ongeldige richting voor horizontale auto!")

        # Ligging verticaal
        elif auto.ligging == 'V':
            if richting == 'Boven':
                if row - stapgrootte >= 0 and all(self.grid[row - i][col] == '_' for i in range(1, stapgrootte + 1)):
                    for i in range(auto.lengte):
                        self.grid[row - stapgrootte + i][col] = auto.naam
                    for i in range(stapgrootte):
                        self.grid[row + auto.lengte - i - 1][col] = '_'
                        row -= stapgrootte
    
            elif richting == 'Onder':
                if row + stapgrootte + auto.lengte - 1 < self.size and all(self.grid[row + auto.lengte + i][col] == '_' for i in range(stapgrootte)):
                    for i in range(auto.lengte):
                        self.grid[row + stapgrootte + i][col] = auto.naam
                    for i in range(stapgrootte):
                        self.grid[row + i][col] = '_'
                    row += stapgrootte
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
                size = int(size_deel[0])  # Het eerste cijfer van de size is de gridgrootte
                spelnummer = int(naam_deel[1].replace('.csv', ''))  # Haal het spelnummer eruit
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
if __name__ == "__main__":
    mapnaam = "gameboards"  # Update naar de map waar je spelborden staan
    pad_naar_csv, size = kies_spelbord(mapnaam)
    if pad_naar_csv:
        autos = lees_csv_bestand(pad_naar_csv)

        speelveld = Grid(size)  # Zorg ervoor dat de size wordt doorgegeven aan Grid
        for auto in autos:
            speelveld.toevoeg_auto(auto)

        speelveld.toon_bord()