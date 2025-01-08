class auto():
    def __init__(self, row, col, lengte, naam, ligging):
        # Coördinaat x en y tuple
        self.positie = (row, col)
        self.lengte = lengte
        self.naam = naam
        # Horizontaal of verticaal
        self.ligging = ligging

class grid():
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
        row -= 1
        col -= 1
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
                
        '''
        Finish maken
        '''
                
    '''
    Variabele 'stappen' toevoegen voor hoeveel stappen je wilt zetten met auto
    '''
    def beweeg_auto(self, auto, richting, stapgrootte):
        row, col = auto.positie
        row -= 1
        col -= 1
        
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
                    for i in range(stapgrootte)
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
        
        '''
        Main game
        '''