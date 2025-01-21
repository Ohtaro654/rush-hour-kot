class Grid():
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
        return self.grid

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
        
            elif richting == 'Onder':
                if row + stapgrootte + auto.lengte - 1 < self.size and all(self.grid[row + auto.lengte + i][col] == '_' for i in range(stapgrootte)):
                    for i in range(auto.lengte):
                        self.grid[row + stapgrootte + i][col] = auto.naam
                    for i in range(stapgrootte):
                        self.grid[row + i][col] = '_'
                    row += stapgrootte
                else:
                    print("Oei botsing of buiten het speelveld, beweging niet mogelijk!")
            else:
                raise ValueError("Ongeldige richting voor verticale auto!")
        # Update positie
        auto.positie = (row, col)

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