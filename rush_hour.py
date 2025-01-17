from flask import Flask, render_template, request, redirect, url_for
from rush_hour_algoritme import *
import matplotlib.pyplot as plt
import os
import csv

app = Flask(__name__)

# globale variable intilialsieren
speelveld = None
autos = []
game_results = []
aantal_zetten = 0
gekozen_spel = None

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

def mogelijke_stappen(random_auto, speelveld):
    ligging = random_auto.ligging
    alle_stappen = []

    # Richtingen bepalen afhankelijk van de ligging
    if ligging == "H":
        richtingen = [("Rechts", 1), ("Links", -1)]
    else:
        richtingen = [("Onder", 1), ("Boven", -1)]

    # Loop door de richtingen en bepaal mogelijke stappen
    for richting, multiplier in richtingen:
        for stappen in range(1, speelveld.size):  # loop tot het einde van het bord
            if not speelveld.is_vrij(random_auto, richting, stappen):
                break  # Stop als een zet niet mogelijk is
            alle_stappen.append(multiplier * stappen)  # Voeg geldige stap toe
    
    print(f"Alle mogelijke stappen voor {random_auto.naam}: {alle_stappen}")  # Debug output
    return alle_stappen
 
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
    global speelveld, autos, gekozen_spel
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
    global speelveld, autos, aantal_zetten  # gebruik de globale variabelen voor speelveld en autos

    # om auto en stappen vragen als je zelf wilt spelen
    auto_naam = request.form['auto_naam'].upper().strip()
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
            # Beweeg de auto
            speelveld.beweeg_auto(auto, richting, abs(stappen))
            aantal_zetten += 1  # Tel de zet
        except ValueError as e:
            # Als er een fout optreedt bij het bewegen
            return render_template('index.html', grid=speelveld.toon_bord(), autos=autos, spellen=os.listdir('gameboards'), huidig_spel=request.args.get('huidig_spel', None), message1=str(e))

    # Controleer of het spel is gewonnen
    if any(auto.naam == "X" and auto.positie[1] + auto.lengte - 1 == speelveld.size - 1 for auto in autos):
        message1 = f"Gefeliciteerd! Het spel is gewonnen in {aantal_zetten} zetten!"
        return render_template('index.html', grid=speelveld.toon_bord(), autos=autos, spellen=os.listdir('gameboards'), huidig_spel=request.args.get('huidig_spel', None), message1=message1)

    # Render de template opnieuw met bijgewerkte data
    return render_template('index.html', grid=speelveld.toon_bord(), autos=autos, spellen=os.listdir('gameboards'), huidig_spel=request.args.get('huidig_spel', None), message1=None)

@app.route('/plot', methods=['GET'])
def plot():  
    global speelveld, autos, gekozen_spel
    # pad naar het spelbord bepalen
    mapnaam = 'gameboards'  
    pad_naar_csv = os.path.join(mapnaam, gekozen_spel)
    size = int(gekozen_spel.split('x')[0].replace('Rushhour', ''))
    
    # haal aantal keer op uit via site
    aantal_keer = request.args.get('aantal_keer')
    aantal_keer = int(aantal_keer)
    
    try:
        moves_list = []  # Om totale zetten per spel op te slaan
        for _ in range(aantal_keer):  # Simuleer het opgegeven aantal spellen
            autos = lees_csv_bestand(pad_naar_csv)
            speelveld = Grid(size)
            for auto in autos:
                speelveld.toevoeg_auto(auto)

            # Start de simulatie en krijg het aantal zetten
            algoritme = request.args.get('algoritme')  # Haal het geselecteerde algoritme op
            try:
                if algoritme == "random_oud":
                    aantal_zetten = random_algoritme_oud(speelveld, autos)
                elif algoritme == "random_new":
                    aantal_zetten = random_algoritme_nieuw(speelveld, autos)
                elif algoritme == "bfs":
                    aantal_zetten = bfs_algoritme(speelveld, autos)
                else:
                    raise ValueError("Onbekend algoritme geselecteerd.")
            except Exception as e:
                return f"Er is een fout opgetreden: {e}"
            # voeg het antal zetten toe aan de lijst
            moves_list.append(aantal_zetten)

        # maak histogram
        plt.figure(figsize=(10, 6))
        plt.hist(moves_list, bins=30, edgecolor='black', alpha=0.75)
        plt.title(f"Distribution of Moves to win {aantal_keer}x")
        plt.xlabel("Number of Moves")
        plt.ylabel("Frequency")
        plt.tight_layout()

        # sla grafiek op
        image_path = os.path.join('static', 'plots', 'simulation_results.png')
        plt.savefig(image_path)
        plt.close()

        # render resultaten
        return render_template('simulation_results.html', plot_url=image_path, huidig_spel=gekozen_spel)
    except Exception as e:
        return f"Fout tijdens simulatie: {e}"
    
@app.route('/restart', methods=['GET'])
def restart_game():
    """
    Reset het spel naar de beginsituatie.
    """
    global speelveld, autos, gekozen_spel

    try:
        pad_naar_csv = os.path.join('gameboards', gekozen_spel)
        size = int(gekozen_spel.split('x')[0].replace('Rushhour', ''))
        autos = lees_csv_bestand(pad_naar_csv)
        speelveld = Grid(size)
        for auto in autos:
            speelveld.toevoeg_auto(auto)

        message = "Het spel is opnieuw gestart!"
    except Exception as e:
        message = f"Fout bij opnieuw starten: {e}"

    return render_template('index.html', grid=speelveld.toon_bord(), autos=autos, message=message)

    
@app.route('/start_algoritme', methods=['GET'])
def start_algoritme():
    """
    Voert het geselecteerde algoritme uit en speelt het spel volledig.
    """
    algoritme = request.args.get('algoritme')  # Haal het geselecteerde algoritme op
    try:
        if algoritme == "random_oud":
            aantal_zetten = random_algoritme_oud(speelveld, autos)
        elif algoritme == "random_new":
            aantal_zetten = random_algoritme_nieuw(speelveld, autos)
        elif algoritme == "bfs":
            aantal_zetten = bfs_algoritme(speelveld, autos)
        else:
            raise ValueError("Onbekend algoritme geselecteerd.")
        
        message = f"Het spel is gewonnen in {aantal_zetten} zetten met het {algoritme}-algoritme!"
    except Exception as e:
        message = f"Er is een fout opgetreden: {e}"

    return render_template('index.html', grid=speelveld.toon_bord(), autos=autos, message=message)


if __name__ == "__main__":
    app.run(debug=True)
