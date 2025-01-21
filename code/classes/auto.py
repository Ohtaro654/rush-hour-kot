class Auto():
    def __init__(self, row, col, lengte, naam, ligging):
        # coordinaat x en y tuple
        self.positie = (row - 1, col - 1)
        self.lengte = lengte
        self.naam = naam
        # horizontaal of verticaal
        self.ligging = ligging