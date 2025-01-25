import copy
import time
from ..helpers import *

def DFAAlgoritme(speelveld, autos):
    # Stack voor depth first
    stack = []
    # Al bezochte staten als set
    visited = set()
    start_tijd = time.time()

    '''
    Bord als tuple in tuple, in de inner tuples hebben we de auto naam en auto posities zitten.
    We hebben inner tuples voor alle auto's voor start grid.
    '''
    begin_bord = tuple(sorted((auto.naam, auto.positie) for auto in autos))
    # Huidig bord en diepte stacken
    stack.append((begin_bord, 0))

    while len(stack) > 0:
        # pop bovenste grid en diepte
        huidig_bord, diepte = stack.pop()

        # Skip als bord al is bezocht
        if huidig_bord in visited:
            continue
        
        # Voeg huidig bord toe aan al bezocht
        visited.add(huidig_bord)

        # Maak grid (nu alleen tuple) om te kijken of het opgelost is
        nieuw_veld = Grid(speelveld.size)
        # Loop over de tuple met naam en positie auto
        for naam, positie in huidig_bord:
            # Vind auto's door ze bij naam te matchen
            auto = next(auto for auto in autos if auto.naam == naam)
            # Krijg de positie van de auto
            auto.positie = positie
            # Voeg auto toe aan grid
            nieuw_veld.toevoeg_auto(auto)

        # Kijk of het opgelost is
        if nieuw_veld.opgelost():
            eind_tijd = time.time()
            print(f"Spel opgelost in {diepte} zetten!")
            print(f"Rentijd: {eind_tijd - start_tijd:.2f} seconden")
            nieuw_veld.toon_bord()
            return diepte, eind_tijd - start_tijd

        '''
        Deze functie laat alle auto's alle bewegingen die zij kunnen maken maken.
        Per auto gaan we kijken hoe ze liggen, en kijken hoeveel stappen ze maximaal kunnen nemen.
        '''
        # Door alle auto's
        for auto in autos:
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
                    stack.append((nieuw_bord, diepte + 1))

    # Als de stack leeg is en geen oplossing gevonden is
    print("Geen oplossing gevonden.")
    return -1, time.time() - start_tijd
