# 🚗 **Rush Hour Project - door TaKuOh**  

## 🧩 **Algoritmen om het spel op te lossen!**  

### 🔍 **Wat is Rush Hour?**  
Rush Hour is een strategisch bordspel waarbij het doel is om een specifieke auto (de rode auto) naar de uitgang te leiden door andere voertuigen die in de weg staan, te verschuiven.  
Deze voertuigen kunnen alleen vooruit of achteruit bewegen binnen hun rij of kolom.  

---

## 🎯 **Ons Project**  
In dit project richten we ons op:  
- Het **implementeren van het spel**, inclusief een dynamische visualisatie om het spel gebruiksvriendelijk te maken.  
- Het **ontwerpen en vergelijken van verschillende algoritmen** die het spel efficiënt kunnen oplossen.  
- Het **creëren van willekeurige borden** die automatisch opgelost kunnen worden.  
- Het **analyseren van de prestaties** van de algoritmen door middel van simulaties.  

---

## 🛠️ **Functies**  
- **Randombord**:  
  - Met deze functie kun je een willekeurig spelbord genereren door simpelweg een bordgrootte te kiezen.  
  - Klik op de knop "Generate" en er wordt een willekeurig bord gemaakt.  
  - Het gegenereerde bord kan vervolgens door een algoritme worden opgelost.  

- **Algoritmen**:  
  - *Random Oud*: Willekeurige zetten zonder verdere optimalisatie.  
  - *Random Nieuw*: Een verbeterde versie die alleen geldige zetten probeert.  
  - *Breadth-First Search (BFS)*: Systematisch zoeken naar de kortste oplossing.  
  - *Depth-First Algoritme (DFA)*: Zoekt dieper en voorkomt herhaling door eerdere borden te onthouden.  
  - *A\*-algoritme*: Heuristisch algoritme dat zoekt op basis van een kostenfunctie (g + h).  
  - *Iterative Deepening Depth-First Search (IDDFS)*: Combineert geheugen-efficiëntie en volledigheid.  

## 🎨 **Visualisatie met Flask**
  - Het bord wordt weergegeven met de daarbijbehorende auto`s die worden onderscheiden door kleur.
  - Visualisatie is gemaakt met Flask waardoor het dus ook interactief is.
  - Histogrammen tonen resultaten van simulaties om algoritmen te vergelijken.  

---

## ⚙️ **Vereisten**  
Alle code is geschreven in **Python 3.12.4**, daarom is het handig dat dit al is geïnstalleerd op je systeem.  
De benodigde libraries kunnen eenvoudig worden geïnstalleerd met:  
```bash
pip install -r requirements.txt
```  

---

## 🕹️ **Het gebruik**  
### **Spel starten en Randombord genereren**  
Om het spel te starten, voer je het volgende commando uit:  
```bash
python3 run.py
```  

In de webinterface kun je:  
1. Een bestaand spelbord selecteren en oplossen zelf of doormiddel van algoritmes.  
2. Een willekeurig bord genereren:  
   - Kies een bordgrootte (bijvoorbeeld 6x6 of 9x9).  
   - Klik op "Generate" om het willekeurige bord te creëren.  
   - Selecteer een algoritme en laat het bord automatisch oplossen.  

Navigeer naar `http://127.0.0.1:5000` in je browser om de webinterface te openen.  

---

© 2025 **TaKuOh**. Alle rechten voorbehouden.  

**Auteurs**: Tarik, Kuba, Otharo
