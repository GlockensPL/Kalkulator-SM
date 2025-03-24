from flask import Flask, request, jsonify
from koszt import koszt

app = Flask(__name__)

def znajdz_koszt(czesc, decision_type, level):
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
        return koszt_rozwoju * ilosc
    return 0

@app.route('/oblicz', methods=['POST'])
def oblicz():
    data = request.json
    fabryki = data['fabryki']
    czesci = ["aero", "skrzynia", "hamulce", "elektronika", "zawieszenie", "niezawodność"]
    
    total_cost = 0
    results = {}

    for czesc in czesci:
        decision = data['decyzje'][czesc]
        level = int(data['poziomy'][czesc])
        ilosc = int(data['ilosci'][czesc])
        koszt_calkowity = oblicz_koszt(czesc, decision, level, fabryki[czesc], ilosc)
        results[czesc] = koszt_calkowity
        total_cost += koszt_calkowity
    
    return jsonify({"koszty": results, "total_cost": total_cost})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)  # Ustawienie portu i hosta
