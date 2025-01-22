import copy
from rush_hour_noflask import *

# Main functie
def iddfs(speelveld, autos, max_diepte=100):
    for diepte in range(max_diepte):
        print(f"Zoek op diepte {diepte}...")
        # Zoek uitgang op iedere diepte
        begin_bord = tuple(sorted((auto.naam, auto.positie) for auto in autos))
        if dls(speelveld, autos, begin_bord, diepte):
            return
    print("We moeten dieper graven.")

# Depth first functie
def dls(speelveld, autos, begin_bord, dieptelimiet):
    stack = [(speelveld, autos, begin_bord, 0)]

    '''
    Hier gebruiken we dict ipv set zoals in depth first. In een dict kunnen we de diepte ook opslaan.
    '''
    visited = {}

    while len(stack) > 0:
        nieuw_veld, huidig_autos, status, huidig_diepte = stack.pop()

        if huidig_diepte > dieptelimiet:
            continue

        # Kijken of het is opgelost
        if nieuw_veld.opgelost():
            print(f"Game solved in {huidig_diepte} moves!")
            nieuw_veld.toon_bord()
            return True

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

                        new_state = tuple(sorted((a.naam, a.positie) for a in autos_copy))

                        stack.append((nieuw_veld_copy, autos_copy, new_state, huidig_diepte + 1))

    return False

if __name__ == "__main__":
    mapnaam = "gameboards"
    pad_naar_csv, size = kies_spelbord(mapnaam)
    if pad_naar_csv:
        autos = lees_csv_bestand(pad_naar_csv)
        speelveld = Grid(size)
        for auto in autos:
            speelveld.toevoeg_auto(auto)

        print("Start iterative deepening depth first algoritme...")
        iddfs(speelveld, autos, max_diepte=100)
