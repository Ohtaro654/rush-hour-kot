from ..helpers import *
import copy
import time

def ASTERalgoritme(speelveld, autos):
    def heuristiek(speelveld, autos, status):
        """
        Heuristiek functie voor het A* algoritme met status.
        - Status 0: Rode auto (doelauto) probeert helemaal naar links te gaan.
        - Status 2: Rode auto probeert de uitgang te bereiken.
        
        Args:
            speelveld: Het speelveldobject.
            autos: Een lijst van auto's op het speelveld.
            status: De huidige status van de heuristiek (0 of 2).
        
        Returns:
            De heuristiekwaarde op basis van de status.
        """
        
        # Vind de rode auto (doelauto)
        rode_auto = next(auto for auto in autos if auto.naam == "X")
        
        if status == 0:
            # Als status 0 is, probeert de rode auto naar links te gaan
            if rode_auto.positie[1] > 0:
                return rode_auto.positie[1]  # Afstand naar de meest linker kolom (kolom 0)
            else:
                # Zodra de rode auto helemaal links staat, status veranderen naar 2
                return 0  # Directe overgang naar de uitgang als de auto links staat
        
        if status == 2:
            # Als status 2 is, gebruikt hij de heuristiek om naar de uitgang te gaan
            return speelveld.size - rode_auto.positie[1]  # Horizontale afstand naar de uitgang
        
        # Als geen van beide statussen van toepassing zijn
        return float('inf')  # Dit zou niet moeten voorkomen


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
        start_heuristiek = heuristiek(speelveld, autos, 0)  # Begin met status 0
        queue.append((0 + start_heuristiek, 0, speelveld, autos, 0))  # (f = g + h, g, speelveld, auto's, status)

        start_tijd = time.time()

        while len(queue) > 0:
            # Haal het bord met de laagste f-waarde (g + h) uit de queue
            f, kosten, huidig_veld, huidig_autos, status = queue.pop(0)  # Zorg dat hier 5 elementen worden uitgepakt

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

                            # Controleer of de rode auto naar links moet gaan (status 0) of de uitgang moet bereiken (status 2)
                            if status == 0 and auto_copy.naam == "X" and auto_copy.positie[1] == 0:
                                # Als de rode auto helemaal naar links is, wijzig status naar 2
                                new_status = 2  # Verander naar de uitgangsstatus

                            # Bereken de heuristiek voor het nieuwe bord
                            new_heuristiek = heuristiek(nieuw_veld_copy, autos_copy, new_status)

                            # Voeg het nieuwe bord toe aan de queue, met nieuwe f-waarde (g + h)
                            queue.append((kosten + 1 + new_heuristiek, kosten + 1, nieuw_veld_copy, autos_copy, new_status))

            # Sorteer de queue op basis van de f-waarde (kleinste f eerst)
            queue.sort(key=lambda x: x[0])

        eind_tijd = time.time()
        ren_tijd = eind_tijd - start_tijd
        print(f"Geen oplossing gevonden. Rentijd: {ren_tijd:.2f} seconden")
    
    # Start het A*-algoritme
    return a_star_algoritme(speelveld, autos)
