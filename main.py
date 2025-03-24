from flask import Flask, request, jsonify
from koszt import koszt

app = Flask(__name__)

def znajdz_koszt(czesc, decision_type, level):
    """Zwraca koszt utrzymania lub rozwoju dla podanego poziomu danej części."""
    for lvl, price in sorted(koszt[czesc][decision_type].items(), reverse=True):
        if level >= lvl:
            return price
    return None

def oblicz_koszt(czesc, decision, level, fabryka_lvl, ilosc):
    if decision == "utrzymanie":
        return znajdz_koszt(czesc, "utrzymanie", level)
    elif decision == "rozwój":
        nowy_level = level + (ilosc * fabryka_lvl)
        koszt_rozwoju = znajdz_koszt(czesc, "rozwój", nowy_level)
        if koszt_rozwoju is None:  # Jeśli koszt rozwoju jest None, zwróć 0 lub inną wartość domyślną
            return 0  # Możesz również zwrócić np. -1, jeśli chcesz wskazać błąd
        return koszt_rozwoju * ilosc
    return 0

@app.route('/oblicz', methods=['POST'])
def oblicz():
    """Przetwarza dane z formularza i oblicza całkowity koszt."""
    data = request.json
    fabryki = data['fabryki']
    czesci = ["aero", "skrzynia", "hamulce", "elektronika", "zawieszenie", "niezawodność"]
    
    total_cost = 0
    results = {}

    for czesc in czesci:
        decision = data['decyzje'][czesc]
        level = int(data['poziomy'][czesc])
        ilosc = int(data['ilosci'][czesc])
        
        # Obliczamy koszt dla danej części
        koszt_calkowity = oblicz_koszt(czesc, decision, level, fabryki[czesc], ilosc)
        
        # Sprawdzamy, czy koszt_calkowity nie jest None
        if koszt_calkowity is not None:
            results[czesc] = koszt_calkowity
            total_cost += koszt_calkowity

    # Zwracamy obliczone koszty w formacie JSON
    return jsonify({"koszty": results, "total_cost": total_cost})

if __name__ == '__main__':
    app.run(debug=True)
