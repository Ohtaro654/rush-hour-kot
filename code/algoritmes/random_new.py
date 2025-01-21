import random
import time
from ..helpers import *

def RandomAlgoritmeNieuw(speelveld, autos):
    aantal_zetten = 0  # Tel het aantal zetten

    start_tijd = time.time()

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
                eind_tijd = time.time()
                ren_tijd = eind_tijd - start_tijd
                print(f"Spel opgelost in {aantal_zetten} zetten!")
                print(f"Rentijd: {ren_tijd:.2f} seconden")
                return aantal_zetten, ren_tijd  # Retourneer het aantal zetten zodra het spel is gewonnen
        
        except Exception as e:
            print(f"Error: {e}")
            break  # Stop bij een fout

    return aantal_zetten  # Return het aantal zetten als het spel is afgelopen