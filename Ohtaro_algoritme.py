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
