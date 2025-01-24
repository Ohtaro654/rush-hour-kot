import time
from ..helpers import *

'''
Iterative deepening depth first algoritme, doet depth first voor iedere diepte.
We gebruiken dict ipv set, omdat het hier niet alleen gaat om de bezochte nodes, maar ook om de dieptes.
'''
def IDDSalgoritme(speelveld, autos, max_diepte=100):
    start_time = time.time()

    # Gaat door elke diepte
    for diepte_limiet in range(max_diepte):
        print(f"Zoekt op diepte: {diepte_limiet}...")
        stack = []
        visited = {}

        begin_bord = tuple(sorted((auto.naam, auto.positie) for auto in autos))
        # Huidig bord en diepte stacken
        stack.append((begin_bord, 0))

        while stack:
            huidig_bord, huidige_diepte = stack.pop()

            if huidige_diepte > diepte_limiet:
                continue

            # Maak grid (nu alleen tuple) om te kijken of het opgelost is
            nieuw_veld = Grid(speelveld.size)
            huidig_autos = []

            # Loop over de tuple met naam en positie auto
            for naam, positie in huidig_bord:
                # Vind auto's door ze bij naam te matchen
                auto = next(auto for auto in autos if auto.naam == naam)
                # Krijg de positie van de auto
                auto.positie = positie
                # Voeg auto toe aan lijst
                huidig_autos.append(auto)
                # Voeg auto toe aan grid
                nieuw_veld.toevoeg_auto(auto)

            # Kijk of het opgelost is
            if nieuw_veld.opgelost():
                print(f"Spel opgelost in {huidige_diepte} zetten!")
                nieuw_veld.toon_bord()
                print(f"Uitgang gevonden op diepte: {diepte_limiet}!")
                runtime = time.time() - start_time
                return huidige_diepte, runtime
            
            if huidig_bord in visited and visited[huidig_bord] <= huidige_diepte:
                continue

            visited[huidig_bord] = huidige_diepte

            '''
            Deze functie laat alle auto's alle bewegingen die zij kunnen maken maken.
            Per auto gaan we kijken hoe ze liggen, en kijken hoeveel stappen ze maximaal kunnen nemen.
            '''
            # Door alle auto's
            for auto in huidig_autos:
                # Kijk naar richtingen auto afhankelijk van ligging
                for richting in ["Links", "Rechts"] if auto.ligging == "H" else ["Boven", "Onder"]:
                    # Bereken max aantal stappen van auto per richting
                    maximale_stappen = nieuw_veld.max_stappen(auto, richting)
                    # Door alle mogelijke stappen van auto
                    for stappen in range(1, maximale_stappen + 1):
                        # Maak list van de tuples in current state zodat we ze kunnen aanpassen
                        nieuw_bord = list(huidig_bord)
                        # Gaat door de list
                        for i, (naam, positie) in enumerate(nieuw_bord):
                            # Wanneer de naam gelijk is aan de auto naam
                            if naam == auto.naam:
                                # Update positie auto positie
                                nieuw_bord[i] = (naam, nieuw_veld.move_position(positie, richting, stappen))
                                # Uit for loop, andere auto's niet meer checken
                                break
                        # Maak van nieuw bord weer tuple
                        nieuw_bord = tuple(sorted(nieuw_bord))

                        # Append deze nieuwe tuple
                        stack.append((nieuw_bord, huidige_diepte + 1))

    runtime = time.time() - start_time
    print("Geen uitgang gevonden op maximale diepte.")
    return None, runtime
