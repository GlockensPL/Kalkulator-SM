from flask import Flask, request, jsonify
from koszt import koszt

app = Flask(__name__)

def przypisz_decyzje(wartosc):
    if wartosc == 0:
        return "degradacja"
    elif wartosc == 0.5:
        return "utrzymanie"
    elif wartosc >= 1:
        return "rozwój"
    return "degradacja"  # Domyślnie traktujmy jako degradację dla wartości poniżej 0.

def znajdz_koszt(czesc, decision_type, level):
    """Zwraca koszt utrzymania lub rozwoju dla podanego poziomu danej części."""
    for lvl, price in sorted(koszt[czesc][decision_type].items(), reverse=True):
        if level >= lvl:
            return price
    return None

def oblicz_koszt(czesc, decision_value, level, fabryka_lvl, ilosc):
    # Przypisujemy decyzję na podstawie wartości liczbowej
    decision = przypisz_decyzje(decision_value)

    if decision == "utrzymanie":
        return znajdz_koszt(czesc, "utrzymanie", level)
    elif decision == "rozwój":
        nowy_level = level + (ilosc * fabryka_lvl)
        koszt_rozwoju = znajdz_koszt(czesc, "rozwój", nowy_level)
        return koszt_rozwoju * ilosc
    elif decision == "degradacja":
        return -znajdz_koszt(czesc, "utrzymanie", level)  # Możesz dodać logikę dla degradacji.
    return 0

@app.route('/oblicz', methods=['POST'])
def oblicz():
    data = request.json
    fabryki = data['fabryki']
    czesci = ["aero", "skrzynia", "hamulce", "elektronika", "zawieszenie", "niezawodność"]
    
    total_cost = 0
    results = {}

    for czesc in czesci:
        # Przekazujemy liczbę jako decyzję
        decision_value = data['decyzje'][czesc]
        level = int(data['poziomy'][czesc])
        ilosc = int(data['ilosci'][czesc])
        koszt_calkowity = oblicz_koszt(czesc, decision_value, level, fabryki[czesc], ilosc)
        results[czesc] = koszt_calkowity
        total_cost += koszt_calkowity
    
    return jsonify({"koszty": results, "total_cost": total_cost})
    return jsonify({"koszty": results, "total_cost": total_cost})
if __name__ == '__main__':
    app.run(debug=True)
