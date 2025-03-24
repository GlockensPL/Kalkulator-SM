from flask import Flask, request, jsonify
from flask_cors import CORS
from koszt import koszt  # Importujemy dane z pliku koszt.py

app = Flask(__name__)
CORS(app)

def oblicz_koszt(czesc, decision_value, level, fabryka, ilosc):
    """
    Funkcja do obliczania kosztu w zależności od części, decyzji, poziomu i liczby jednostek.
    Uwzględnia zmiany kosztów na każdym poziomie.

    :param czesc: nazwa części
    :param decision_value: decyzja (0.5 utrzymanie, 1, 2, 3... rozwój)
    :param level: aktualny poziom części
    :param fabryka: słownik z kosztami
    :param ilosc: liczba jednostek
    :return: całkowity koszt
    """
    total_cost = 0  # Zmienna do sumowania całkowitego kosztu

    if decision_value == 0:  # Degradacja
        # Obliczamy koszt w przypadku degradacji
        return -znajdz_koszt(czesc, "utrzymanie", level)
    elif decision_value == 0.5:  # Utrzymanie
        # Obliczamy koszt dla utrzymania
        return -znajdz_koszt(czesc, "utrzymanie", level) * ilosc
    else:  # Rozwój
        # Musimy obliczyć koszt po kolei, przechodząc przez każdy poziom
        current_level = level
        while current_level < level + ilosc:
            # Zmieniamy koszt w zależności od poziomu
            if current_level >= 60:
                cost = znajdz_koszt(czesc, "rozwój", current_level)  # Używamy kosztu rozwoju dla poziomu >= 60
            else:
                cost = znajdz_koszt(czesc, "rozwój", current_level)  # Koszt rozwoju przed poziomem 60
            total_cost += cost  # Sumujemy koszty dla każdego poziomu
            current_level += 1  # Przechodzimy do następnego poziomu

    return total_cost  # Zwracamy całkowity koszt

def znajdz_koszt(czesc, decision, level):
    """
    Funkcja, która zwraca koszt na podstawie części, decyzji i poziomu.
    Uwaga: Koszty są oparte na poziomie i decyzji (utrzymanie/rozwój).

    :param czesc: nazwa części
    :param decision: decyzja (utrzymanie/rozwój)
    :param level: poziom części
    :return: koszt dla danej części, decyzji i poziomu
    """
    # Sprawdzamy w słowniku, czy koszt jest dostępny
    try:
        return koszt[czesc][decision][level]
    except KeyError:
        print(f"Nie znaleziono kosztu dla: {czesc}, {decision}, {level}")
        return 0  # Zwracamy 0, jeśli koszt nie został znaleziony
        
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
