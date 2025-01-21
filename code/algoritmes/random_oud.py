import random
import time
from ..helpers import *

def RandomAlgoritmeOud(speelveld, autos):
    auto_lijst = []
    
    start_tijd = time.time()

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
                eind_tijd = time.time()
                ren_tijd = eind_tijd - start_tijd
                print(f"Spel opgelost in {diepte} zetten!")
                print(f"Rentijd: {ren_tijd:.2f} seconden")
                return aantal_zetten, ren_tijd
        except ValueError:
            # Ongeldige zet, probeer opnieuw
            continue