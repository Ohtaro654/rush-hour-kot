from code.classes.auto import Auto
from code.classes.grid import Grid
import random

# voor elke bord autos
auto_settings = {
    6: {
        9, 14
    },
    9: {
        19, 24
    },
    12: {
        35, 43
    }
}

def generate_board(size):
    """
    functie om random bord te genereren voor elke size
    """
    # haal het aantal autos op voor de gekozen size
    min_cars, max_cars = auto_settings[size]
    num_cars = random.randint(min_cars, max_cars)

    # initialiseer speelveld
    speelveld = Grid(size)

    # stel de vaste rij in voor de rode auto X
    if size == 6:
        x_row = 2  # Rij 3 0,1,2
    elif size == 9:
        x_row = 4
    elif size == 12:
        x_row = 5
    else:
        raise ValueError("Ongeldige grootte voor de rode auto.")

    # rode auto plaatsen
    # een random kolom kiezen, maar niet de laatste (uitgang)
    x_start_col = random.randint(0, size - 3)  # Laatste 2 kolommen vermijden
    x_auto = Auto(x_row + 1, x_start_col + 1, 2, "X", "H")
    speelveld.toevoeg_auto(x_auto)

    # Lijst van autos
    autos = [x_auto]

    # functie om namen aan autos toe te wijzen
    def generate_car_name(index):
        """
        geeft auto namen en skipt x, want die is bestaat al
        """
        name = ""
        while index >= 0:
            name = chr(65 + (index % 26)) + name
            index = index // 26 - 1
        if name == "X":  # Sla rode auto 'X' over
            return generate_car_name(index + 1)
        return name

    # Plaats de overige auto's
    car_index = 1 # rode auto al opgelteld
    while len(autos) < num_cars:
        naam = generate_car_name(car_index)
        lengte = random.choice([2, 2, 3])  # Lengte 2 voor autos en 3 voor vrachtwagens
        ligging = random.choice(["H", "V"])  # random richting
        valid_position = False

        for _ in range(100):  # probeer 100 keer een geldige positie te vinden
            if ligging == "H":
                row = random.randint(0, size - 1)
                start_col = random.randint(0, size - lengte)
                # horizontale auto mag niet op zelfde rij liggen als rode auto
                if row == x_row:
                    continue  # Sla over als de rij dezelfde is als de rij van "X"
                # Controleer of de ruimte vrij is
                if all(speelveld.grid[row][col] == "_" for col in range(start_col, start_col + lengte)):
                    auto = Auto(row + 1, start_col + 1, lengte, naam, "H")
                    speelveld.toevoeg_auto(auto)
                    autos.append(auto)
                    valid_position = True
                    break
            else:  # Verticaal
                col = random.randint(0, size - 1)
                start_row = random.randint(0, size - lengte)
                # controleer of de ruimte vrij is
                if all(speelveld.grid[row][col] == "_" for row in range(start_row, start_row + lengte)):
                    auto = Auto(start_row + 1, col + 1, lengte, naam, "V")
                    speelveld.toevoeg_auto(auto)
                    autos.append(auto)
                    valid_position = True
                    break

        if valid_position:
            car_index += 1
            print({car_index})

    return speelveld, autos, speelveld.toon_bord()
