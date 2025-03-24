import tkinter as tk
from tkinter import messagebox
from koszt import koszt


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
    else:
        return 0


def oblicz_i_wyswietl():
    try:
        fabryki = {
            "aero": int(aero_fab.get()),
            "elektronika": int(elektronika_fab.get()),
            "zawieszenie": int(zawieszenie_fab.get()),
            "niezawodność": int(niezawodnosc_fab.get()),
            "skrzynia": int(telemetria_fab.get()),
            "hamulce": int(telemetria_fab.get())  # Hamulce dzielą fabrykę ze skrzynią
        }

        total_cost = 0
        for czesc in czesci:
            decision = decyzje[czesc].get()
            level = int(poziomy[czesc].get())
            ilosc = int(ilosci[czesc].get())
            koszt_calkowity = oblicz_koszt(czesc, decision, level, fabryki[czesc], ilosc)
            total_cost += koszt_calkowity

        messagebox.showinfo("Wynik", f"Łączny koszt: {total_cost} $")
    except ValueError:
        messagebox.showerror("Błąd", "Wprowadź poprawne wartości!")


czesci = ["aero", "skrzynia", "hamulce", "elektronika", "zawieszenie", "niezawodność"]
root = tk.Tk()
root.title("Kalkulator kosztów")

tk.Label(root, text="Poziomy fabryk:").grid(row=0, column=0, columnspan=2)
aero_fab = tk.Entry(root)
elektronika_fab = tk.Entry(root)
zawieszenie_fab = tk.Entry(root)
niezawodnosc_fab = tk.Entry(root)
telemetria_fab = tk.Entry(root)
aero_fab.grid(row=1, column=1)
elektronika_fab.grid(row=2, column=1)
zawieszenie_fab.grid(row=3, column=1)
niezawodnosc_fab.grid(row=4, column=1)
telemetria_fab.grid(row=5, column=1)

tk.Label(root, text="Aero:").grid(row=1, column=0)
tk.Label(root, text="Elektronika:").grid(row=2, column=0)
tk.Label(root, text="Zawieszenie:").grid(row=3, column=0)
tk.Label(root, text="Niezawodność:").grid(row=4, column=0)
tk.Label(root, text="Telemetria (skrzynia i hamulce):").grid(row=5, column=0)

decyzje = {}
poziomy = {}
ilosci = {}
row = 6
tk.Label(root, text="Część").grid(row=row, column=0)
tk.Label(root, text="Decyzja").grid(row=row, column=1)
tk.Label(root, text="Poziom").grid(row=row, column=2)
tk.Label(root, text="Ilość").grid(row=row, column=3)

row += 1
for czesc in czesci:
    tk.Label(root, text=czesc).grid(row=row, column=0)
    decyzje[czesc] = tk.StringVar(value="utrzymanie")
    tk.OptionMenu(root, decyzje[czesc], "utrzymanie", "rozwój").grid(row=row, column=1)
    poziomy[czesc] = tk.Entry(root)
    poziomy[czesc].grid(row=row, column=2)
    ilosci[czesc] = tk.Entry(root)
    ilosci[czesc].grid(row=row, column=3)
    row += 1

tk.Button(root, text="Oblicz", command=oblicz_i_wyswietl).grid(row=row, column=0, columnspan=4)

root.mainloop()
