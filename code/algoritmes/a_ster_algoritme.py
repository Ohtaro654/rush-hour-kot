from ..helpers import *
import heapq
import copy
import time

def ASTERalgoritme(speelveld, autos):
    def heuristiek(speelveld, autos):
        """
        Heuristiek functie voor het A* algoritme.
        We gebruiken het aantal horizontale stappen van de rode auto (doelauto)
        naar de uitgang als heuristiek.
        """
        # Vind de rode auto (doelauto)
        rode_auto = next(auto for auto in autos if auto.naam == "X")
        # Aantal stappen van de rode auto naar de uitgang
        return speelveld.size - rode_auto.positie[1]  # Horizontale afstand naar de uitgang

    def heuristiek2(speelveld, autos):
        """Estimate the number of moves to solve the puzzle."""
        for auto in autos:
            if auto.naam == "X":
                x_exit = auto.positie[1] + auto.lengte - 1
                blocking_cars = 0
                for y in range(x_exit + 1, speelveld.size):
                    if speelveld.toon_het_bord()[auto.positie[0]][y] != 0:
                        blocking_cars += 1
                return blocking_cars
        return float('inf')

    def a_star_algoritme(speelveld, autos):
        """
        A* algoritme met heuristiek (gebruikmakend van een priority queue).
        """
        # Priority queue voor A* (houdt bord en kosten bij)
        queue = []
        # Set van bezochte borden
        visited = set()
        # Beginbord als tuple van auto's en posities
        begin_bord = tuple(sorted((auto.naam, auto.positie) for auto in autos))
        
        zetten = 0
        # Startkosten zijn 0, en begin heuristiek wordt berekend
        start_heuristiek = heuristiek(speelveld, autos)
        queue.append((0 + start_heuristiek, 0, speelveld, autos, begin_bord))  # (f = g + h, g, speelveld, auto's, status)

        start_tijd = time.time()

        while len(queue) > 0:
            # Haal het bord met de laagste f-waarde (g + h) uit de queue
            f, kosten, huidig_veld, huidig_autos, status = queue.pop(0)

            # Kijk of het huidige veld is opgelost
            if huidig_veld.opgelost():
                eind_tijd = time.time()
                ren_tijd = eind_tijd - start_tijd
                print(f"Spel opgelost in {zetten} zetten!")
                print(f"Rentijd: {ren_tijd:.2f} seconden")
                speelveld.grid = huidig_veld.grid
                speelveld.toon_bord() # laat het eindbord zien
                return zetten, ren_tijd

            # Skip status (tuple) als het al is bezocht
            if status in visited:
                continue

            # Voeg status toe aan de visited set
            visited.add(status)

            # Alle mogelijke zetten van auto's
            for auto in huidig_autos:
                # Door mogelijke richtingen
                for richting in ["Links", "Rechts"] if auto.ligging == 'H' else ["Boven", "Onder"]:
                    # Aantal stappen die auto's kunnen zetten
                    for stappen in range(1, speelveld.size):
                        if huidig_veld.is_vrij(auto, richting, stappen):
                            # Maak een kopie van het bord en de auto's
                            nieuw_veld_copy = copy.deepcopy(huidig_veld)
                            autos_copy = copy.deepcopy(huidig_autos)

                            # Zoek de auto die we willen bewegen
                            auto_copy = next(a for a in autos_copy if a.naam == auto.naam)

                            # Beweeg de auto
                            nieuw_veld_copy.beweeg_auto(auto_copy, richting, stappen)
                            zetten += 1
                            # Maak een nieuwe status (bord als tuple)
                            new_status = tuple(sorted((a.naam, a.positie) for a in autos_copy))

                            # Bereken de heuristiek voor het nieuwe bord
                            new_heuristiek = heuristiek(nieuw_veld_copy, autos_copy)

                            # Voeg het nieuwe bord toe aan de queue, met nieuwe f-waarde (g + h)
                            queue.append((kosten + 1 + new_heuristiek, kosten + 1, nieuw_veld_copy, autos_copy, new_status))

            # Sorteer de queue op basis van de f-waarde (kleinste f eerst)
            queue.sort(key=lambda x: x[0])

        eind_tijd = time.time()
        ren_tijd = eind_tijd - start_tijd
        print(f"Geen oplossing gevonden. Rentijd: {ren_tijd:.2f} seconden")
    
    # Start het A*-algoritme
    a_star_algoritme(speelveld, autos)
