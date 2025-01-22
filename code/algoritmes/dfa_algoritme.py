import copy
import time
from ..helpers import *


def DFAAlgoritme(speelveld, autos):
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
            # copy winnende bord naar originele speelveld
            speelveld.grid = nieuw_veld.grid
            speelveld.toon_bord()  # laat het eindbord zien
            return zetten, ren_tijd

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
    ren_tijd = eind_tijd - start_tijd
    print(f"Geen oplossing gevonden. Rentijd: {ren_tijd:.2f} seconden")