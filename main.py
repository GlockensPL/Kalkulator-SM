from flask import Flask, request, jsonify
from koszt import koszt  # Importujemy dane z pliku koszt.py

app = Flask(__name__)

def znajdz_koszt(czesc, decision_type, level):
    print(f"Sprawdzam koszt dla części: {czesc}, decyzja: {decision_type}, poziom: {level}")
    
    if czesc not in koszt:
        print(f"Brak danych dla części: {czesc}")
        return None

    if decision_type not in koszt[czesc]:
        print(f"Brak danych dla decyzji: {decision_type} w części: {czesc}")
        return None

    for lvl, price in sorted(koszt[czesc][decision_type].items(), reverse=True):
        print(f"Sprawdzam: poziom {lvl}, cena {price}")
        if level >= lvl:
            print(f"Znaleziono koszt: {price}")
            return price
    
    print("Nie znaleziono kosztu.")
    return None

def oblicz_koszt(czesc, decision_value, level, fabryka_lvl, ilosc):
    if decision_value == 0:
        print(f"Degradacja dla {czesc}")
        return -znajdz_koszt(czesc, "utrzymanie", level)  # Degradacja
    elif decision_value == 0.5:
        print(f"Utrzymanie dla {czesc}")
        return znajdz_koszt(czesc, "utrzymanie", level)  # Utrzymanie
    elif decision_value >= 1:
        print(f"Rozwój dla {czesc}")
        nowy_level = level + (ilosc * fabryka_lvl)
        koszt_rozwoju = znajdz_koszt(czesc, "rozwój", nowy_level)
        if koszt_rozwoju is not None:
            return koszt_rozwoju * ilosc  # Rozwój
    return 0

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
