class auto():
    def __init__(self, positie, lengte, naam, ligging):
        # Coördinaat x en y tuple
        self.positie = positie
        self.lengte = lengte
        self.naam = naam
        # Horizontaal of verticaal
        self.ligging = ligging

    def beweeg_auto(self, richting):
        row, col = self.positie
        # Ligging horizontaal
        if self.ligging == 'H':
            if richting == 'Links':
                col += 1
            elif richting == 'Rechts':
                col -= 1
            else:
                raise ValueError("Ongeldige richting voor horizontale auto!")

        # Ligging verticaal
        elif self.ligging == 'V':
            if richting == 'Boven':
                row += 1
            elif richting == 'Onder':
                row -= 1
            else:
                raise ValueError("Ongeldige richting voor verticale auto!")
        # Update positie
        self.positie = (row, col)
        
class grid():
    def __init__(self):
        # Maakt grid van 6x6 met _
        self.grid = [['_'] * 6 for _ in range(6)]

    def toevoeg_auto(self, auto):
        row, col = auto.positie
        if auto.ligging == 'H':
            # Kijken of auto past op bord
            if col + auto.lengte > 6:
                raise ValueError("Past niet op het bord!")
            # Kijken of niet overlapt
            for i in range(col, col + auto.lengte):
                if self.grid[row][i] != '_':
                    raise ValueError("Auto overlapt!")
            # Voeg auto toe
            for i in range(col, col + auto.lengte):
                self.grid[row][i] = auto.naam

        elif auto.ligging == 'V':
            # Kijken of auto past op bord
            if row + auto.lengte > 6:
                raise ValueError("Past niet op het bord!")
            # Kijken of niet overlapt
            for j in range(row, row + auto.lengte):
                if self.grid[j][col] != '_':
                    raise ValueError("Auto overlapt!")
            # Voeg auto toe
            for j in range(row, row + auto.lengte):
                self.grid[j][col] = auto.naam