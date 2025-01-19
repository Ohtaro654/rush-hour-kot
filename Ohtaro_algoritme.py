from rush_hour_noflask import *
import copy

def dfa_algoritme(speelveld, autos):
    # Stack voor depth first
    stack = []
    # Dictionary al bezochte borden (geen repetitie)
    visited = {}
    # Aantal zetten bijhouden
    zetten = 0

    # Bord nu als tuple met tuples van auto's met naam en positie
    begin_bord = tuple(sorted((auto.naam, auto.positie) for auto in autos))
    # Append speelveld, auto's, bord nu en aantal zetten en diepte
    stack.append((speelveld, autos, begin_bord, 0))

    while len(stack) > 0:
        # Pop tuple
        nieuw_veld, huidig_autos, status, diepte = stack.pop()

        # Kijk of het nieuwe veld is opgelost
        if nieuw_veld.opgelost():
            print(f"Spel opgelost in {diepte} zetten!")
            nieuw_veld.toon_bord()  # Show the final board
            return
        
                # Skip status (tuple) over als het al is bezocht
        if status in visited and visited[status] <= diepte:
            continue

        # De tuple als key, diepte als value
        visited[status] = diepte

        for auto in huidig_autos:
            # Door mogelijke richtingen
            for richting in ["Links", "Rechts"] if auto.ligging == 'H' else ["Boven", "Onder"]:
                # Aantal stappen die auto's kunnen zetten
                for stappen in range(1, speelveld.size):
                    # Kijken of auto kan bewegen
                    if nieuw_veld.is_vrij(auto, richting, stappen):
                        print(f"Mogeijke stap: {auto.naam} beweegt {richting} met {stappen} stap.")