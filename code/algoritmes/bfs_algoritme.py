from collections import deque
import copy
import time
from ..helpers import *

def BFSAlgoritme(speelveld, autos):

    queue = deque([(copy.deepcopy(speelveld), copy.deepcopy(autos), 0, [])])
    visited = set([tuple(tuple(row) for row in speelveld.toon_bord())])

    start_tijd = time.time()

    while queue:
        current_speelveld, current_autos, zetten, move_history = queue.popleft()

        # check of gesolved is
        for auto in current_autos:
            if auto.naam == "X" and auto.positie[1] + auto.lengte - 1 == current_speelveld.size - 1:
                eind_tijd = time.time()
                ren_tijd = eind_tijd - start_tijd
                print(f"Spel opgelost in {zetten} zetten!")
                print(f"Rentijd: {ren_tijd:.2f} seconden")
                # zoja zetten op echte spelbord uitvoeren
                for move in move_history:
                    speelveld.beweeg_auto(*move)
                return zetten, ren_tijd

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

    eind_tijd = time.time()
    ren_tijd = eind_tijd - start_tijd
    print(f"Geen oplossing gevonden. Rentijd: {ren_tijd:.2f} seconden")
    return -1