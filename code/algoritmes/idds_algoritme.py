import copy
import time
from ..helpers import *

def IDDSalgoritme(speelveld, autos, max_diepte=100):
    """
    IDDS-algoritme: Iteratief Verdiepende Diepte search.
    """
    start_tijd = time.time()
    zetten = 0

    for diepte in range(max_diepte):
        print(f"Zoek op diepte {diepte}...")

        begin_bord = tuple(sorted((auto.naam, auto.positie) for auto in autos))
        stack = [(speelveld, autos, begin_bord, 0)]

        '''
        Hier gebruiken we dict ipv set zoals in depth first. In een dict kunnen we de diepte ook opslaan.
        '''
        visited = {}

        while len(stack) > 0:
            nieuw_veld, huidig_autos, status, huidig_diepte = stack.pop()

            if huidig_diepte > diepte:
                continue

            # Kijken of het spel is opgelost
            if nieuw_veld.opgelost():
                eind_tijd = time.time()
                ren_tijd = eind_tijd - start_tijd
                print(f"Spel opgelost in {zetten} zetten!")
                print(f"Rentijd: {ren_tijd:.2f} seconden")
                speelveld.grid = nieuw_veld.grid
                speelveld.toon_bord() # laat het eindbord zien
                return zetten, ren_tijd

            if status in visited and visited[status] <= huidig_diepte:
                continue

            visited[status] = huidig_diepte

            for auto in huidig_autos:
                for richting in ["Links", "Rechts"] if auto.ligging == 'H' else ["Boven", "Onder"]:
                    for stappen in range(1, speelveld.size):
                        if nieuw_veld.is_vrij(auto, richting, stappen):
                            nieuw_veld_copy = copy.deepcopy(nieuw_veld)
                            autos_copy = copy.deepcopy(huidig_autos)

                            auto_copy = next(a for a in autos_copy if a.naam == auto.naam)
                            nieuw_veld_copy.beweeg_auto(auto_copy, richting, stappen)
                            zetten += 1

                            new_state = tuple(sorted((a.naam, a.positie) for a in autos_copy))

                            stack.append((nieuw_veld_copy, autos_copy, new_state, huidig_diepte + 1))

    ren_tijd = time.time() - start_tijd
    print("We moeten dieper graven.")
    return -1, ren_tijd
