import csv
import os

class Auto:
    def __init__(self, row, col, lengte, naam, ligging):
        # Coördinaat x en y tuple, aangepast voor 1-gebaseerde indexering
        self.positie = (row - 1, col - 1)  # Omzetten naar 0-gebaseerde index
        self.lengte = lengte
        self.naam = naam
        self.ligging = ligging  # Horizontaal (H) of verticaal (V)

class Grid:
    def __init__(self):
        # Maakt een grid van 6x6 met '_'
        self.grid = [['_'] * 6 for _ in range(6)]

    def voeg_auto_toe(self, auto):
        row, col = auto.positie
        if auto.ligging == 'H':
            # Controleer of de auto past op het bord
            if col + auto.lengte > 6:
                raise ValueError("De auto past niet op het bord!")
            # Controleer op overlap
            for i in range(col, col + auto.lengte):
                if self.grid[row][i] != '_':
                    raise ValueError("De auto overlapt met een andere auto!")
            # Voeg de auto toe aan het grid
            for i in range(col, col + auto.lengte):
                self.grid[row][i] = auto.naam

        elif auto.ligging == 'V':
            # Controleer of de auto past op het bord
            if row + auto.lengte > 6:
                raise ValueError("De auto past niet op het bord!")
            # Controleer op overlap
            for j in range(row, row + auto.lengte):
                if self.grid[j][col] != '_':
                    raise ValueError("De auto overlapt met een andere auto!")
            # Voeg de auto toe aan het grid
            for j in range(row, row + auto.lengte):
                self.grid[j][col] = auto.naam

    def toon_bord(self):
        for row in self.grid:
            print(' '.join(row))

    def beweeg_auto(self, auto, richting):
        row, col = auto.positie
        if auto.ligging == 'H':
            if richting == 'Links':
                if col > 0 and self.grid[row][col - 1] == '_':
                    # Verplaats de auto naar links
                    self.grid[row][col - 1] = auto.naam
                    self.grid[row][col + auto.lengte - 1] = '_'
                    auto.positie = (row, col - 1)
            elif richting == 'Rechts':
                if col + auto.lengte < 6 and self.grid[row][col + auto.lengte] == '_':
                    # Verplaats de auto naar rechts
                    self.grid[row][col + auto.lengte] = auto.naam
                    self.grid[row][col] = '_'
                    auto.positie = (row, col + 1)
            else:
                raise ValueError("Ongeldige richting voor een horizontale auto!")

        elif auto.ligging == 'V':
            if richting == 'Boven':
                if row > 0 and self.grid[row - 1][col] == '_':
                    # Verplaats de auto naar boven
                    self.grid[row - 1][col] = auto.naam
                    self.grid[row + auto.lengte - 1][col] = '_'
                    auto.positie = (row - 1, col)
            elif richting == 'Onder':
                if row + auto.lengte < 6 and self.grid[row + auto.lengte][col] == '_':
                    # Verplaats de auto naar onder
                    self.grid[row + auto.lengte][col] = auto.naam
                    self.grid[row][col] = '_'
                    auto.positie = (row + 1, col)
            else:
                raise ValueError("Ongeldige richting voor een verticale auto!")

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

    print("Beschikbare spelborden:")
    for i, bestand in enumerate(bestanden, start=1):
        print(f"{i}: {bestand}")

    while True:
        try:
            keuze = int(input(f"Kies een spelbord (1-{len(bestanden)}): "))
            if 1 <= keuze <= len(bestanden):
                return os.path.join(mapnaam, bestanden[keuze - 1])
            else:
                print("Ongeldige keuze, probeer opnieuw.")
        except ValueError:
            print("Voer een geldig nummer in.")

# Voorbeeldgebruik
if __name__ == "__main__":
    mapnaam = "gameboards"  # Update naar de map waar je spelborden staan
    pad_naar_csv = kies_spelbord(mapnaam)
    if pad_naar_csv:
        autos = lees_csv_bestand(pad_naar_csv)

        speelveld = Grid()
        for auto in autos:
            speelveld.voeg_auto_toe(auto)

        speelveld.toon_bord()
