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
        self.grid = [['_'] * 6 for _ in range(6)]

    def toevoeg_auto(self, auto):

