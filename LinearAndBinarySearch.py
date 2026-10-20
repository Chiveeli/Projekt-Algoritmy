"""
Tabuľka 1 – porovnanie Linear Search a Binary Search

Zadanie:
- pre N = 10 000 000 vytvoriť jednu dátovú sadu a 10 náhodných hodnôt
- tie isté hodnoty použiť pre LS aj BS
- pre N = 100 000 000 vytvoriť inú dátovú sadu a iných 10 hodnôt
- merať čas a počet porovnaní
- priemery a odhady zapisovať v Exceli pomocou vzorcov
"""

import bisect
import json
import random
import time


# =====================================================================
#  LINEAR SEARCH
# =====================================================================

def linear_search(arr, target):
    start_time = time.perf_counter()
    comparisons = 0

    for i in range(len(arr)):
        comparisons += 1
        if arr[i] == target:
            end_time = time.perf_counter()
            return i, comparisons, (end_time - start_time) * 1000

    end_time = time.perf_counter()
    return -1, comparisons, (end_time - start_time) * 1000


# =====================================================================
#  BINARY SEARCH
# =====================================================================

def binary_search(arr, target):
    start_time = time.perf_counter()
    comparisons = 0

    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2

        comparisons += 1
        if arr[mid] == target:
            end_time = time.perf_counter()
            return mid, comparisons, (end_time - start_time) * 1000

        comparisons += 1
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    end_time = time.perf_counter()
    return -1, comparisons, (end_time - start_time) * 1000


# =====================================================================
#  GENEROVANIE ZORADENEJ DÁTOVEJ SADY S OPAKOVANÍM
# =====================================================================

def vytvor_zoznam(n):
    """
    Vytvorí už zoradený zoznam bez volania sort().
    Umožňuje opakovanie čísel (krok 0) aj medzery (krok 2 až 9),
    vďaka čomu sa časť hľadaných hodnôt v zozname nenájde.
    Pre n = 10 000 000 je rozsah približne 0 až 45 000 000.
    """
    hodnota = random.randint(0, 9)
    arr = [hodnota]

    for _ in range(1, n):
        hodnota += random.randint(0, 9)
        arr.append(hodnota)

    return arr


# =====================================================================
#  GENEROVANIE 10 HĽADANÝCH HODNÔT Z CELÉHO ROZSAHU
# =====================================================================

def je_v_zozname(arr, hodnota):
    """Rýchla kontrola (bisect) - používa sa len pri výbere hodnôt, nie pri meraní."""
    i = bisect.bisect_left(arr, hodnota)
    return i < len(arr) and arr[i] == hodnota


def vytvor_hladane_hodnoty(arr):
    """
    Vygeneruje 10 náhodných hodnôt z celého rozsahu <min, max>.
    Dobre zvolená sada má 1 až 5 nájdených a 5 až 9 nenájdených hodnôt,
    preto hodnoty generujeme znova, kým táto podmienka neplatí.
    """
    minimum = arr[0]
    maximum = arr[-1]

    while True:
        hodnoty = [random.randint(minimum, maximum) for _ in range(10)]
        najdene = sum(1 for h in hodnoty if je_v_zozname(arr, h))
        if 1 <= najdene <= 5:
            return hodnoty


# =====================================================================
#  MERANIE
# =====================================================================

def meraj(search_funkcia, arr, hladane_hodnoty):
    vysledky = []

    for hodnota in hladane_hodnoty:
        pozicia, porovnania, cas_ms = search_funkcia(arr, hodnota)
        vysledky.append((hodnota, pozicia, cas_ms, porovnania))

    return vysledky


def vypis_vysledky(n, nazov, vysledky):
    print(f"\n{nazov} N = {n:,}".replace(",", " "))
    print("-" * 60)
    print("Hodnota\tPozicia\tCas [ms]\tPorovnania")

    for hodnota, pozicia, cas_ms, porovnania in vysledky:
        print(f"{hodnota}\t{pozicia}\t{cas_ms:.6f}\t{porovnania}")


def vypis_priemery(label, ls_vysledky, bs_vysledky):
    ls_priemer_cas = sum(r[2] for r in ls_vysledky) / len(ls_vysledky)
    ls_priemer_porovnania = sum(r[3] for r in ls_vysledky) / len(ls_vysledky)

    bs_priemer_cas = sum(r[2] for r in bs_vysledky) / len(bs_vysledky)
    bs_priemer_porovnania = sum(r[3] for r in bs_vysledky) / len(bs_vysledky)

    print(f"\nPriemer {label}")
    print(f"LS čas: {ls_priemer_cas:.10f} ms")
    print(f"LS porovnania: {ls_priemer_porovnania}")
    print(f"BS čas: {bs_priemer_cas:.10f} ms")
    print(f"BS porovnania: {bs_priemer_porovnania}")


def spusti_sadu(n, nazov_sady):
    arr = vytvor_zoznam(n)
    hladane_hodnoty = vytvor_hladane_hodnoty(arr)

    ls_vysledky = meraj(linear_search, arr, hladane_hodnoty)
    bs_vysledky = meraj(binary_search, arr, hladane_hodnoty)

    vypis_vysledky(n, "Linear Search", ls_vysledky)
    vypis_vysledky(n, "Binary Search", bs_vysledky)
    vypis_priemery(nazov_sady, ls_vysledky, bs_vysledky)

    najdene = sum(1 for x in ls_vysledky if x[1] != -1)
    nenajdene = sum(1 for x in ls_vysledky if x[1] == -1)

    print(f"\nKontrola sady {nazov_sady}:")
    print(f"Nájdené hodnoty: {najdene}")
    print(f"Nenájdené hodnoty: {nenajdene}")

    return arr, hladane_hodnoty, ls_vysledky, bs_vysledky


# =====================================================================
#  HLAVNÝ PROGRAM
# =====================================================================

if __name__ == "__main__":
    vysledky = {}

    for n, nazov_sady in ((10_000_000, "N1"), (100_000_000, "N2")):
        arr, hladane, ls, bs = spusti_sadu(n, nazov_sady)
        vysledky[nazov_sady] = {
            "n": n,
            "min": arr[0],
            "max": arr[-1],
            "hladane": hladane,
            "LS": [{"hodnota": h, "pozicia": p, "cas_ms": c, "porovnania": k} for h, p, c, k in ls],
            "BS": [{"hodnota": h, "pozicia": p, "cas_ms": c, "porovnania": k} for h, p, c, k in bs],
        }
        del arr                     # uvoľníme pamäť pred generovaním väčšej sady

    with open("vysledky_tabulka1.json", "w", encoding="utf-8") as f:
        json.dump(vysledky, f, ensure_ascii=False, indent=2)

    print("\nVýsledky uložené do vysledky_tabulka1.json")
    print("Odhady pre N = 100 000 000 sú v Exceli ako vzorce, nie ručne napísané hodnoty.")
