from rush_hour import *
import random

def random_algoritme(speelveld, autos):
    auto_lijst = []
    
    for auto in autos:
        auto_lijst.append(auto.naam)
    
    while True:
        try:
            #genereer een random auto
            random_auto = random.randint(0, len(auto_lijst) - 1)
            #genereer random stappen
            random_stappen = random.randint(-1*size + 1, size - 1)
            auto_naam = auto_lijst[random_auto]
            auto_naam = auto_naam.upper()
            # Controleer of de auto bestaat
            auto = next((a for a in autos if a.naam == auto_naam), None)

           
            
            
            if not auto:
                print("Auto niet gevonden. Probeer opnieuw.")
                continue
            
            
        

            # Vraag om het aantal blokjes om te verplaatsen
            stappen = random_stappen
            
            # Bepaal de richting op basis van de ligging van de auto
            if stappen > 0 and auto.ligging == "H":
                richting = "Rechts"
            elif stappen < 0 and auto.ligging == "H":
                richting = "Links"
            elif stappen > 0 and auto.ligging == "V":
                richting = "Onder"
            else:
                richting = "Boven"

            # Roep jouw beweeg_auto functie aan
            speelveld.beweeg_auto(auto, richting, abs(stappen))
            
            # Beweging succesvol, stop de loop
            break
        except ValueError:
            print("Ongeldige invoer")


# Game loop voorbeeld
if __name__ == "__main__":
    mapnaam = "gameboards"  # Map waar spelborden staan
    pad_naar_csv, size = kies_spelbord(mapnaam)
    if pad_naar_csv:
        autos = lees_csv_bestand(pad_naar_csv)
        speelveld = Grid(size)
        for auto in autos:
            speelveld.toevoeg_auto(auto)

        aantal_zetten = 0
        
        while True:
            speelveld.toon_bord()
            random_algoritme(speelveld, autos)
            aantal_zetten += 1

            # Controleer of de X aan de rechterkant is om het spel te winnen
            if any(auto.naam == "X" and auto.positie[1] + auto.lengte - 1 == size - 1 for auto in autos):
                speelveld.toon_bord()
                print("Gefeliciteerd! Je hebt het spel gewonnen!")
                print(f"Aantal zetten is: {aantal_zetten}")
                break