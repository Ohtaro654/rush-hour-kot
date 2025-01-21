import csv
import os
from code.classes.auto import Auto
from code.classes.grid import Grid

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
        elif algoritme == "dfa":
            aantal_zetten = dfa_algoritme(speelveld, autos)
        else:
            raise ValueError("Onbekend algoritme geselecteerd.")
        
        message = f"Het spel is gewonnen in {aantal_zetten} zetten met het {algoritme}-algoritme!"
    except Exception as e:
        message = f"Er is een fout opgetreden: {e}"

    return render_template('index.html', grid=speelveld.toon_bord(), autos=autos, message=message)
