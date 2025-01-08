class auto():
    def __init__(self, positie, lengte, naam, ligging):
        # Coördinaat x en y tuple
        self.positie = positie
        self.lengte = lengte
        self.naam = naam
        # Horizontaal of verticaal
        self.ligging = ligging

class grid():
    '''
    Variabele size (voor grid) toevoegen.
    '''
    def __init__(self):
        # Maakt grid van 6x6 met _
        self.grid = [['_'] * 6 for _ in range(6)]


        '''
        Auto's toevoegen uit een csv file
        '''
    def toevoeg_auto(self, auto):
        row, col = auto.positie
        if auto.ligging == 'H':
            # Kijken of auto past op bord
            if col + auto.lengte > 6:
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
            if row + auto.lengte > 6:
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
    def beweeg_auto(self, auto, richting):
        row, col = auto.positie
        # Ligging horizontaal
        if auto.ligging == 'H':
            if richting == 'Links':
                # binnen grid en vakje links is _
                if col - 1 >= 0 and self.grid[row][col - 1] == '_':
                    # Eentje naar links
                    for i in range(auto.lengte):
                        self.grid[row][col - 1 + i] = auto.naam
                    # Meest rechtse wordt leeg
                    self.grid[row][col + auto.lengte - 1] = '_'
                    # Positieverandering
                    col -= 1
                    
            elif richting == 'Rechts':
                if col + 1 < 6 and self.grid[row][col + 1] == '_':
                    for i in range(auto.lengte):
                        self.grid[row][col + 1 + i] = auto.naam
                    # Meest linkse wordt leeg
                    self.grid[row][col] = '_'
                    # Positieverandering
                    col += 1
            else:
                raise ValueError("Ongeldige richting voor horizontale auto!")

        # Ligging verticaal
        elif auto.ligging == 'V':
            if richting == 'Boven':
                if row - 1 >= 0 and self.grid[row - 1][col] == '_':
                    for i in range(auto.lengte):
                        self.grid[row - 1 + i][col] = auto.naam
                    self.grid[row + auto.lengte - 1][col] = '_'
                    row -= 1
                    
            elif richting == 'Onder':
                if row + 1 < 6 and self.grid[row + 1][col] == '_':
                    for i in range(auto.lengte):
                        self.grid[row + 1 + i][col] = auto.naam
                    self.grid[row][col] = '_'
                    row += 1
            else:
                raise ValueError("Ongeldige richting voor verticale auto!")
        # Update positie
        auto.positie = (row, col)
        
        '''
        Main game
        '''