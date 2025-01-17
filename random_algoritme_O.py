import matplotlib.pyplot as plt
import random
from rush_hour import *

def randomnew(speelveld, autos):
    while True:
        try:
            random_auto = random.choice(autos)
            random_stappen = mogelijke_stappen(random_auto, speelveld)
            if not random_stappen:
                break  # No valid moves for the selected auto
            random_stap = random.choice(random_stappen)

            auto = random_auto
            stappen = random_stap

            if stappen > 0 and auto.ligging == "H":
                richting = "Rechts"
            elif stappen < 0 and auto.ligging == "H":
                richting = "Links"
            elif stappen > 0 and auto.ligging == "V":
                richting = "Onder"
            else:
                richting = "Boven"

            speelveld.beweeg_auto(auto, richting, abs(stappen))
        except Exception as e:
            print(f"Error: {e}")
            break

def mogelijke_stappen(random_auto, speelveld):
    row, col = random_auto.positie
    ligging = random_auto.ligging
    alle_stappen = []

    if ligging == "H":
        richtingen = [("Rechts", 1), ("Links", -1)]
    else:
        richtingen = [("Onder", 1), ("Boven", -1)]

    for richting, multiplier in richtingen:
        for stappen in range(1, speelveld.size):
            if not speelveld.is_vrij(random_auto, richting, stappen):
                break
            alle_stappen.append(multiplier * stappen)

    return alle_stappen

def simulate_game(mapnaam, num_simulations=1000):
    moves_list = []
    pad_naar_csv, size = kies_spelbord(mapnaam)

    if pad_naar_csv:
        for _ in range(num_simulations):
            autos = lees_csv_bestand(pad_naar_csv)
            speelveld = Grid(size)
            for auto in autos:
                speelveld.toevoeg_auto(auto)

            aantal_zetten = 0
            while True:
                randomnew(speelveld, autos)
                aantal_zetten += 1

                if any(auto.naam == "X" and auto.positie[1] + auto.lengte - 1 == size - 1 for auto in autos):
                    moves_list.append(aantal_zetten)
                    break

    return moves_list

def plot_moves(moves_list):
    plt.hist(moves_list, bins=30, edgecolor='black', alpha=0.75)
    plt.title("Distribution of Moves to Win")
    plt.xlabel("Number of Moves")
    plt.ylabel("Frequency")
    plt.show()

if __name__ == "__main__":
    mapnaam = "gameboards"  # Map waar spelborden staan
    num_simulations = 1000
    moves_list = simulate_game(mapnaam, num_simulations)
    plot_moves(moves_list)
