from rush_hour import *
import random

def random_algoritme(speelveld, autos):
    auto_lijst = []
    
    for auto in autos:
        auto_lijst.append(auto.naam)
    
    aantal_zetten = 0

    while True:
        try:
            #genereer een random auto
            random_auto = random.randint(0, len(auto_lijst) - 1)
            #genereer random stappen
            random_stappen = random.randint(-1*speelveld.size + 1, speelveld.size - 1)
            auto_naam = auto_lijst[random_auto]
            auto_naam = auto_naam.upper()
            # Controleer of de auto bestaat
            auto = next((a for a in autos if a.naam == auto_naam), None)
            
            if not auto:
                print("Auto niet gevonden. Probeer opnieuw.")
                continue
            
            # Vraag om het aantal blokjes om te verplaatsen
            stappen = random_stappen
            
            # Bepaal de richting op basis van de ligging van de auto
            if stappen > 0 and auto.ligging == "H":
                richting = "Rechts"
            elif stappen < 0 and auto.ligging == "H":
                richting = "Links"
            elif stappen > 0 and auto.ligging == "V":
                richting = "Onder"
            else:
                richting = "Boven"

            # Roep jouw beweeg_auto functie aan
            speelveld.beweeg_auto(auto, richting, abs(stappen))
            aantal_zetten += 1
            # Controleer of het spel is gewonnen
            if any(a.naam == "X" and a.positie[1] + a.lengte - 1 == speelveld.size - 1 for a in autos):
                return aantal_zetten
        except ValueError:
            # Ongeldige zet, probeer opnieuw
            continue

def mogelijke_stappen(random_auto, speelveld):
    row, col = random_auto.positie
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

def randomnew(speelveld, autos):
    aantal_zetten = 0  # Tel het aantal zetten

    while True:
        try:
            # Kies een willekeurige auto
            random_auto = random.choice(autos)
            random_stappen = mogelijke_stappen(random_auto, speelveld)
            
            if not random_stappen:  # Als geen stappen beschikbaar zijn
                print(f"Geen beschikbare stappen voor {random_auto.naam}.")
                continue  # Kies een andere auto

            random_stap = random.choice(random_stappen)

            print(f"Beschikbare stappen voor {random_auto.naam}: {random_stappen}")
            print(f"Random stap gekozen: {random_stap}")

            # Bepaal de richting op basis van de gekozen stap
            if random_stap > 0 and random_auto.ligging == "H":
                richting = "Rechts"
            elif random_stap < 0 and random_auto.ligging == "H":
                richting = "Links"
            elif random_stap > 0 and random_auto.ligging == "V":
                richting = "Onder"
            else:
                richting = "Boven"

            # Voer de zet uit
            speelveld.beweeg_auto(random_auto, richting, abs(random_stap))

            aantal_zetten += 1  # Verhoog het aantal zetten

            # Controleer of het spel is gewonnen
            if any(auto.naam == "X" and auto.positie[1] + auto.lengte - 1 == speelveld.size - 1 for auto in autos):
                print("Het spel is gewonnen!")
                return aantal_zetten  # Retourneer het aantal zetten zodra het spel is gewonnen
        
        except Exception as e:
            print(f"Error: {e}")
            break  # Stop bij een fout

    return aantal_zetten  # Return het aantal zetten als het spel is afgelopen
