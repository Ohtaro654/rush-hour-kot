from flask import Flask, render_template, request, redirect, url_for
from rush_hour_algoritme import *
import os
import csv

app = Flask(__name__)

# globale variable intilialsieren
speelveld = None
autos = []

class Auto():
    def __init__(self, row, col, lengte, naam, ligging):
        # coordinaat x en y tuple
        self.positie = (row - 1, col - 1)
        self.lengte = lengte
        self.naam = naam
        # horizontaal of verticaal
        self.ligging = ligging

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

@app.route('/', methods=['GET', 'POST'])
def index():
    global speelveld, autos
    mapnaam = 'gameboards'
    spellen = [f for f in os.listdir(mapnaam) if f.startswith("Rushhour") and f.endswith(".csv")]
    spellen.sort()
    
    if request.method == 'POST':
        # verwerk keuze van de user
        gekozen_spel = request.form['spel']
        pad_naar_csv = os.path.join(mapnaam, gekozen_spel)
        size = int(gekozen_spel.split('x')[0].replace('Rushhour', ''))
        autos = lees_csv_bestand(pad_naar_csv)
        speelveld = Grid(size)
        for auto in autos:
            speelveld.toevoeg_auto(auto)

        return render_template('index.html', grid=speelveld.toon_bord(), autos=autos, spellen=spellen, huidig_spel=gekozen_spel)
    
    return render_template('index.html', grid=None, autos=None, spellen=spellen, huidig_spel=None)

@app.route('/vraag_en_beweeg', methods=['POST'])
def vraag_en_beweeg():
    """
    Vraag de gebruiker om een auto te verplaatsen en voer de beweging uit.
    """
    global speelveld, autos  # gebruik de globale variabelen voor speelveld en autos

    # om auto en stappen vragen als je zelf wilt spelen
    auto_naam = request.form['auto_naam'].upper()
    stappen = int(request.form['stappen'])

    # controleer eerst of de auto bestaat
    auto = next((a for a in autos if a.naam == auto_naam), None)
    if auto:
        # bepal de richting op basis van de ligging van de auto
        if stappen > 0 and auto.ligging == "H":
            richting = "Rechts"
        elif stappen < 0 and auto.ligging == "H":
            richting = "Links"
        elif stappen > 0 and auto.ligging == "V":
            richting = "Onder"
        else:
            richting = "Boven"

        try:
            # beweeg de auto
            speelveld.beweeg_auto(auto, richting, abs(stappen))
        except ValueError as e:
            print(e)

    # render de template opnieuw met de bijgewerkte positie van auto
    return render_template('index.html', grid=speelveld.toon_bord(), autos=autos, spellen=os.listdir('gameboards'),huidig_spel=request.args.get('huidig_spel', None))

@app.route('/start_algoritme')
def start_algoritme():
    """
    Voert het random algoritme uit en speelt het spel volledig.
    """
    try:
        aantal_zetten = random_algoritme(speelveld, autos)
        message = f"Het spel is gewonnen in {aantal_zetten} zetten!"
    except Exception as e:
        message = f"Er is een fout opgetreden: {e}"

    return render_template('index.html', grid=speelveld.toon_bord(), autos=autos, message=message)

if __name__ == "__main__":
    app.run(debug=True)
