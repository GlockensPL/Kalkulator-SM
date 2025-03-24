from flask import Flask, request, jsonify
from koszt import koszt  # Importujemy dane z pliku koszt.py

app = Flask(__name__)

def znajdz_koszt(czesc, decision_type, level):
    """
    Funkcja zwraca koszt w zależności od decyzji i poziomu dla danej części.
    """
    # Znajdź odpowiedni przedział poziomu (np. 40-49, 50-59)
    if level < 50:
        level_key = 40
    elif level < 60:
        level_key = 50
    elif level < 70:
        level_key = 60
    elif level < 80:
        level_key = 70
    elif level < 90:
        level_key = 80
    else:
        level_key = 90

    # Pobierz koszt w zależności od decyzji
    koszt = koszt.get(czesc, {}).get(decision_type, {}).get(level_key)
    
    if koszt is None:
        print(f"Nie znaleziono kosztu dla {czesc} ({decision_type}) na poziomie {level_key}")
    return koszt

def oblicz_koszt(czesc, decision_value, level, fabryki, ilosc):
    """
    Funkcja oblicza całkowity koszt na podstawie części, decyzji, poziomu i ilości.
    """
    if decision_value == 0:
        # Degradacja: zmiana poziomu o jeden w dół
        level -= 10
        if level < 40:  # Sprawdzamy, czy nie schodzimy poniżej poziomu 40
            level = 40
        decision_type = "utrzymanie"  # W przypadku degradacji zawsze korzystamy z utrzymania
    elif decision_value == 0.5:
        # Utrzymanie: nie zmieniamy poziomu
        decision_type = "utrzymanie"
    else:
        # Rozwój: zmiana poziomu o jeden w górę
        level += 10
        if level > 90:  # Sprawdzamy, czy nie przekraczamy poziomu 90
            level = 90
        decision_type = "rozwój"  # W przypadku rozwoju korzystamy z rozwoju

    # Pobieramy koszt na podstawie zmienionego poziomu i decyzji
    koszt_rozwoju = znajdz_koszt(czesc, decision_type, level)
    
    if koszt_rozwoju is None:
        return 0  # Zwracamy 0, jeśli nie znaleziono kosztu
    
    # Obliczamy całkowity koszt
    koszt_calkowity = koszt_rozwoju * ilosc
    return koszt_calkowity

@app.route('/oblicz', methods=['POST'])
def oblicz():
    data = request.json
    fabryki = data['fabryki']
    czesci = ["aero", "skrzynia", "hamulce", "elektronika", "zawieszenie", "niezawodność"]
    
    total_cost = 0
    results = {}

    for czesc in czesci:
        decision_value = float(data['decyzje'][czesc])  # Teraz traktujemy decyzje jako float
        level = int(data['poziomy'][czesc])
        ilosc = int(data['ilosci'][czesc])
        koszt_calkowity = oblicz_koszt(czesc, decision_value, level, fabryki[czesc], ilosc)
        
        # Sprawdzamy, czy koszt jest None, aby uniknąć błędu typu
        if koszt_calkowity is not None:
            results[czesc] = koszt_calkowity
            total_cost += koszt_calkowity
    
    return jsonify({"koszty": results, "total_cost": total_cost})

if __name__ == '__main__':
    app.run(debug=True)
