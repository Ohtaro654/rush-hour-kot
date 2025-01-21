from collections import deque
from rush_hour import *
import time
import copy
import random

def random_algoritme_oud(speelveld, autos):
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

def random_algoritme_nieuw(speelveld, autos):
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

def bfs_algoritme(speelveld, autos):

    queue = deque([(copy.deepcopy(speelveld), copy.deepcopy(autos), 0, [])])
    visited = set([tuple(tuple(row) for row in speelveld.toon_bord())])

    while queue:
        current_speelveld, current_autos, zetten, move_history = queue.popleft()

        # check of gesolved is
        for auto in current_autos:
            if auto.naam == "X" and auto.positie[1] + auto.lengte - 1 == current_speelveld.size - 1:
                print(f"Oplossing gevonden in {zetten} zetten!")
                # zoja zetten op echte spelbord uitvoeren
                for move in move_history:
                    speelveld.beweeg_auto(*move)
                return zetten

        # alle mogelijke bewegingn generen
        for auto in current_autos:
            stappen_opties = mogelijke_stappen(auto, current_speelveld)
            for stappen in stappen_opties:
                richting = "Rechts" if stappen > 0 and auto.ligging == "H" else \
                           "Onder" if stappen > 0 else \
                           "Links" if auto.ligging == "H" else "Boven"

                if current_speelveld.is_vrij(auto, richting, abs(stappen)):
                    # kopie maken van huidige stand
                    nieuw_speelveld = copy.deepcopy(current_speelveld)
                    nieuwe_autos = copy.deepcopy(current_autos)

                    # auto verplaatsen
                    nieuw_auto = next(a for a in nieuwe_autos if a.naam == auto.naam)
                    nieuw_speelveld.beweeg_auto(nieuw_auto, richting, abs(stappen))

                    # aan queue toevoegen als het nog niet gevisited was
                    bord_str = tuple(tuple(row) for row in nieuw_speelveld.toon_bord())
                    if bord_str not in visited:
                        visited.add(bord_str)
                        queue.append((nieuw_speelveld, nieuwe_autos, zetten + 1, move_history + [(auto, richting, abs(stappen))]))

    print("Geen oplossing gevonden pik!")
    return -1

def dfa_algoritme(speelveld, autos):
    # Stack voor depth first
    stack = []
    # Dictionary al bezochte borden (geen repetitie)
    visited = set()
    # Aantal zetten bijhouden
    zetten = 0

    # Bord nu als tuple met tuples van auto's met naam en positie
    begin_bord = tuple(sorted((auto.naam, auto.positie) for auto in autos))
    # Append speelveld, auto's, bord nu en aantal zetten en diepte
    stack.append((speelveld, autos, begin_bord, 0))

    start_tijd = time.time()

    while len(stack) > 0:
        # Pop tuple
        nieuw_veld, huidig_autos, status, diepte = stack.pop()

        # Kijk of het nieuwe veld is opgelost
        if nieuw_veld.opgelost():
            eind_tijd = time.time()
            ren_tijd = eind_tijd - start_tijd
            print(f"Spel opgelost in {diepte} zetten!")
            print(f"Rentijd: {ren_tijd:.2f} seconden")
            nieuw_veld.toon_bord()  # Show the final board
            return zetten

        # Skip status (tuple) over als het al is bezocht
        if status in visited:
            continue

        # De tuple als key, diepte als value
        visited.add(status)

        # Alle zetten van auto's
        for auto in huidig_autos:
            # Door mogelijke richtingen
            for richting in ["Links", "Rechts"] if auto.ligging == 'H' else ["Boven", "Onder"]:
                # Aantal stappen die auto's kunnen zetten
                for stappen in range(1, speelveld.size):
                    if nieuw_veld.is_vrij(auto, richting, stappen):
                        if stappen < 2:
                            print(f"Mogeijke stap: {auto.naam} beweegt {richting} met {stappen} stap.")
                        else:
                            print(f"Mogeijke stap: {auto.naam} beweegt {richting} met {stappen} stappen.")
                        '''
                        Nu alles met deepcopy, we willen originele bord niet veranderen.
                        '''

                        # Kopie van veld en auto's
                        nieuw_veld_copy = copy.deepcopy(nieuw_veld)
                        autos_copy = copy.deepcopy(huidig_autos)

                        # Welke auto te bewegen
                        auto_copy = next(a for a in autos_copy if a.naam == auto.naam)

                        # Beweeg de auto
                        nieuw_veld_copy.beweeg_auto(auto_copy, richting, stappen)

                        # tuple met bord als een tuple
                        new_status = tuple(sorted((a.naam, a.positie) for a in autos_copy))

                        # Push het nieuwe bord op de stack
                        stack.append((nieuw_veld_copy, autos_copy, new_status, diepte + 1))

                    else:
                        # Als het niet vrij is
                        break

        zetten += 1
        print(f"Beweeg {zetten}: diepte {diepte}")
        nieuw_veld.toon_bord()

    eind_tijd = time.time()
    rentijd = eind_tijd - start_tijd
    print(f"Geen oplossing gevonden. Rentijd: {ren_tijd:.2f} seconden")