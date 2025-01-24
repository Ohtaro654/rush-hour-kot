from ..helpers import *
import heapq
import copy
import time

def ASTERalgoritme(speelveld, autos):
    def heuristiek(speelveld, autos, status):
        """
        Heuristiek functie met drie statussen:
        - Status 0: Rode auto probeert helemaal naar links te gaan.
        - Status 1: Rode auto probeert naar achteren te gaan.
        - Status 2: Rode auto probeert de uitgang te bereiken.
        """
        # Vind de rode auto (doelauto)
        rode_auto = next(auto for auto in autos if auto.naam == "X")

        if status == 0:
            # Status 0: Rode auto probeert helemaal naar links
            if rode_auto.positie[1] > 0:
                return rode_auto.positie[1]  # Afstand naar de meest linker kolom (kolom 0)
            else:
                # Zodra de rode auto helemaal links staat, verander status naar 1
                status = 1

        if status == 1:
            # Status 1: Rode auto probeert naar achteren te gaan
            # Controleer of er auto's zijn die blokkeren aan de achterkant (kolom 0)
            blokkades_achter = any(
                auto.ligging == 'V' and auto.positie[0] == rode_auto.positie[0]
                and 0 <= auto.positie[1] < rode_auto.positie[1]
                for auto in autos
            )
            if blokkades_achter:
                return rode_auto.positie[1]  # Afstand tot de eerste blokkade
            else:
                # Zodra er geen blokkades zijn, verander status naar 2
                status = 2

        if status == 2:
            # Status 2: Rode auto probeert naar de uitgang te gaan
            afstand = speelveld.size - rode_auto.positie[1]
            # Tel het aantal auto's die de uitgang blokkeren
            hindernissen = sum(
                1 for auto in autos
                if auto.ligging == 'V' and auto.positie[0] == rode_auto.positie[0]
                and rode_auto.positie[1] < auto.positie[1] < speelveld.size
            )
            return afstand + hindernissen

        # Onverwachte situatie, geef een hoge waarde
        return float('inf')

    def a_star_algoritme(speelveld, autos):
        """
        A* algoritme met geavanceerde heuristiek (inclusief status).
        """
        # Priority queue voor A*
        queue = []
        visited = set()
        zetten = 0

        # Beginstatus en heuristiek
        begin_bord = tuple(sorted((auto.naam, auto.positie) for auto in autos))
        status = 0  # Begin met status 0
        start_heuristiek = heuristiek(speelveld, autos, status)
        queue.append((0 + start_heuristiek, 0, speelveld, autos, begin_bord, status))  # Voeg status toe aan queue

        start_tijd = time.time()

        while len(queue) > 0:
            # Haal het bord met de laagste f-waarde (g + h) uit de queue
            f, kosten, huidig_veld, huidig_autos, bord_status, status = queue.pop(0)

            # Controleer of het huidige veld is opgelost
            if huidig_veld.opgelost():
                eind_tijd = time.time()
                ren_tijd = eind_tijd - start_tijd
                print(f"Spel opgelost in {kosten} zetten!")
                print(f"Rentijd: {eind_tijd - start_tijd:.2f} seconden")
                speelveld.grid = huidig_veld.grid
                speelveld.toon_bord() # laat het eindbord zien
                return zetten, ren_tijd

            # Als de status al is bezocht, sla deze over
            if bord_status in visited:
                continue

            # Voeg de huidige status toe aan de bezochte set
            visited.add(bord_status)

            # Genereer mogelijke zetten
            for auto in huidig_autos:
                for richting in ["Links", "Rechts"] if auto.ligging == 'H' else ["Boven", "Onder"]:
                    for stappen in range(1, speelveld.size):
                        if huidig_veld.is_vrij(auto, richting, stappen):
                            # Maak een kopie van het bord en auto's
                            nieuw_veld_copy = copy.deepcopy(huidig_veld)
                            autos_copy = copy.deepcopy(huidig_autos)
                            auto_copy = next(a for a in autos_copy if a.naam == auto.naam)

                            # Beweeg de auto
                            nieuw_veld_copy.beweeg_auto(auto_copy, richting, stappen)
                            zetten += 1
                            # Bereken de nieuwe status
                            nieuwe_status = tuple(sorted((a.naam, a.positie) for a in autos_copy))

                            # Bereken de heuristiek
                            nieuwe_heuristiek = heuristiek(nieuw_veld_copy, autos_copy, status)

                            # Voeg toe aan de queue
                            queue.append((kosten + 1 + nieuwe_heuristiek, kosten + 1, nieuw_veld_copy, autos_copy, nieuwe_status, status))

            # Sorteer de queue op f-waarde
            queue.sort(key=lambda x: x[0])

        eind_tijd = time.time()
        print(f"Geen oplossing gevonden. Rentijd: {eind_tijd - start_tijd:.2f} seconden")
    
    # Start het A*-algoritme
    a_star_algoritme(speelveld, autos)
