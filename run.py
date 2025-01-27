from flask import Flask, render_template, request, redirect, url_for, jsonify
from code.classes.grid import Grid
from code.classes.auto import Auto
from code.helpers import *
from code.randombord import generate_board
from code.algoritmes.random_oud import RandomAlgoritmeOud
from code.algoritmes.random_new import RandomAlgoritmeNieuw
from code.algoritmes.bfs_algoritme import BFSAlgoritme
from code.algoritmes.dfa_algoritme import DFAAlgoritme
from code.algoritmes.idds_algoritme import IDDSalgoritme
from code.algoritmes.a_ster_algoritme import ASTERalgoritme
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# globale variable intilialsieren
speelveld = None
autos = []
game_results = []
aantal_zetten = 0
gekozen_spel = None
original_speelveld = None
original_autos = None

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    homepagina waar user bordspel kan kiezen
    """
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
    """
    functie om resultaten van algoritmes te plotten
    """
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
                    aantal_zetten = RandomAlgoritmeOud(speelveld, autos)
                elif algoritme == "random_new":
                    aantal_zetten = RandomAlgoritmeNieuw(speelveld, autos)
                elif algoritme == "bfs":
                    aantal_zetten = BFSAlgoritme(speelveld, autos)
                elif algoritme == "dfa":
                    aantal_zetten = DFAAlgoritme(speelveld, autos)
                elif algoritme == "idds":
                    aantal_zetten = IDDSalgoritme(speelveld, autos)
                elif algoritme == "aster":
                    aantal_zetten = ASTERalgoritme(speelveld, autos)
                else:
                    raise ValueError("Onbekend algoritme geselecteerd.")
            except Exception as e:
                return f"Er is een fout opgetreden: {e}"
            # voeg het antal zetten toe aan de lijst
            moves_list.append(aantal_zetten)

        # maak histogram
        plt.figure(figsize=(10, 6))
        plt.hist(moves_list, bins=30, edgecolor='black', alpha=0.75)
        plt.title(f"Distribution of Moves to win {aantal_keer}x with {algoritme}")
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
    global speelveld, autos, gekozen_spel, original_speelveld, original_autos

    try:
        if gekozen_spel:
            pad_naar_csv = os.path.join('gameboards', gekozen_spel)
            size = int(gekozen_spel.split('x')[0].replace('Rushhour', ''))
            autos = lees_csv_bestand(pad_naar_csv)
            speelveld = Grid(size)
            for auto in autos:
                speelveld.toevoeg_auto(auto)

            message = "Het spel is opnieuw gestart!"

        elif original_speelveld and original_autos:  # controleer of een random bord actief is
            #gGenereer een nieuw random bord
            size = original_speelveld.size  # gebruik dezelfde grootte als het vorige bord

            speelveld, autos, grid = generate_board(size)
            message = "Een nieuw random bord is gegenereerd!"
        else:
            # geen spel om te resetten
            raise ValueError("Er is geen actief spel om opnieuw te starten. Kies of genereer eerst een bord.")

    except Exception as e:
        message = f"Fout bij opnieuw starten: {e}"

    return render_template('index.html', grid=speelveld.toon_bord(), autos=autos, message=message)

@app.route('/generate_random', methods=['POST'])
def generate_random():
    """
    random rush hour bordspel genereren
    """
    global speelveld, autos, gekozen_spel, original_autos, original_speelveld
    size = int(request.form.get('size', 6))

    # functie om randombord te genereren
    speelveld, autos, grid = generate_board(size)

    original_speelveld = Grid(size)  # maak een nieuwe kopie van het grid
    for auto in autos:
        original_speelveld.toevoeg_auto(auto)
    original_autos = [Auto(a.positie[0], a.positie[1], a.lengte, a.naam, a.ligging) for a in autos]

    return render_template('index.html', grid=grid, autos=autos, spellen=None, huidig_spel=None, message="Random bord gegenereerd!")

    
@app.route('/start_algoritme', methods=['GET'])
def start_algoritme():
    """
    Voert het geselecteerde algoritme uit en speelt het spel volledig.
    """
    algoritme = request.args.get('algoritme')  # Haal het geselecteerde algoritme op
    try:
        if algoritme == "random_oud":
            aantal_zetten, tijd = RandomAlgoritmeOud(speelveld, autos)
        elif algoritme == "random_new":
            aantal_zetten, tijd = RandomAlgoritmeNieuw(speelveld, autos)
        elif algoritme == "bfs":
            aantal_zetten, tijd = BFSAlgoritme(speelveld, autos)
        elif algoritme == "dfa":
            aantal_zetten, tijd = DFAAlgoritme(speelveld, autos)
        elif algoritme == "idds":
            aantal_zetten, tijd = IDDSalgoritme(speelveld, autos)
        elif algoritme == "aster":
            aantal_zetten, tijd = ASTERalgoritme(speelveld, autos)
        else:
            raise ValueError("Onbekend algoritme geselecteerd.")
        
        message = f"Het spel is gewonnen in {tijd:.2f} seconden met {aantal_zetten} zetten door het {algoritme}-algoritme!"
    except Exception as e:
        message = f"Er is een fout opgetreden: {e}"

    return render_template('index.html', grid=speelveld.toon_bord(), autos=autos, message=message)

if __name__ == '__main__':
    app.run(debug=False)