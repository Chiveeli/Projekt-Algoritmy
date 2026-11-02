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
import math
import random
import statistics
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


def anomalie(vysledky):
    """Indexy meraní, ktorých čas na 1 porovnanie je väčší ako 2 × medián sady."""
    casy = [cas_ms / porovnania for _, _, cas_ms, porovnania in vysledky]
    median = statistics.median(casy)
    return {i for i, cas in enumerate(casy) if cas > 2 * median}


def priemery(vysledky):
    """Vráti priemerný čas (bez anomálií) a priemerný počet porovnaní."""
    zle = anomalie(vysledky)
    casy = [r[2] for i, r in enumerate(vysledky) if i not in zle]
    return sum(casy) / len(casy), sum(r[3] for r in vysledky) / len(vysledky)


def vypis_tabulku(n, nazov_sady, ls_vysledky, bs_vysledky):
    zle_ls, zle_bs = anomalie(ls_vysledky), anomalie(bs_vysledky)

    print(f"\nTabuľka 1 – sada {nazov_sady} = {n:_}".replace("_", " "))
    print(f"{'':>3} {'Hľadaná':>12} | {'LS pozícia':>11} {'LS čas (ms)':>13} {'LS porovnania':>14} | "
          f"{'BS pozícia':>11} {'BS čas (ms)':>13} {'BS porovnania':>14}")

    for i, (ls, bs) in enumerate(zip(ls_vysledky, bs_vysledky)):
        ls_cas = f"{ls[2]:.3f}" + ("*" if i in zle_ls else "")
        bs_cas = f"{bs[2]:.4f}" + ("*" if i in zle_bs else "")
        print(f"{i + 1:>3} {ls[0]:>12} | {ls[1]:>11} {ls_cas:>13} {ls[3]:>14} | "
              f"{bs[1]:>11} {bs_cas:>13} {bs[3]:>14}")

    ls_cas, ls_por = priemery(ls_vysledky)
    bs_cas, bs_por = priemery(bs_vysledky)
    print(f"Priemer: LS čas {ls_cas:.3f} ms, LS porovnania {ls_por:.1f}, "
          f"BS čas {bs_cas:.4f} ms, BS porovnania {bs_por:.2f}")

    najdene = sum(1 for x in ls_vysledky if x[1] != -1)
    print(f"Nájdené hodnoty: {najdene}, nenájdené hodnoty: {len(ls_vysledky) - najdene}")
    if zle_ls or zle_bs:
        print("* časová anomália (čas na 1 porovnanie > 2 × medián), nie je v priemere")


def vypis_odhad(n1, n2, ls1, bs1, ls2, bs2):
    """Odhad pre väčšiu sadu z priemerov menšej sady a porovnanie so skutočnosťou."""
    k_ls = n2 / n1                              # O(N)
    k_bs = math.log2(n2) / math.log2(n1)        # O(log N)

    print(f"\nOdhad pre N2 = {n2:_} (z priemerov N1)".replace("_", " "))
    print(f"{'':16} {'odhad':>16} {'skutočnosť':>16} {'odhad / skut.':>14}")
    for nazov, zaklad, skutocnost, k, fmt in (
            ("LS čas (ms)", ls1[0], ls2[0], k_ls, ".3f"),
            ("LS porovnania", ls1[1], ls2[1], k_ls, ".1f"),
            ("BS čas (ms)", bs1[0], bs2[0], k_bs, ".4f"),
            ("BS porovnania", bs1[1], bs2[1], k_bs, ".2f")):
        odhad = zaklad * k
        print(f"{nazov:16} {odhad:>16{fmt}} {skutocnost:>16{fmt}} {odhad / skutocnost:>14.1%}")


def spusti_sadu(n, nazov_sady):
    arr = vytvor_zoznam(n)
    hladane_hodnoty = vytvor_hladane_hodnoty(arr)

    ls_vysledky = meraj(linear_search, arr, hladane_hodnoty)
    bs_vysledky = meraj(binary_search, arr, hladane_hodnoty)

    vypis_tabulku(n, nazov_sady, ls_vysledky, bs_vysledky)

    return arr, hladane_hodnoty, ls_vysledky, bs_vysledky


# =====================================================================
#  HLAVNÝ PROGRAM
# =====================================================================

if __name__ == "__main__":
    vysledky = {}
    priemery_sady = {}

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
        priemery_sady[nazov_sady] = (priemery(ls), priemery(bs))
        del arr                     # uvoľníme pamäť pred generovaním väčšej sady

    vypis_odhad(vysledky["N1"]["n"], vysledky["N2"]["n"], *priemery_sady["N1"], *priemery_sady["N2"])

    with open("vysledky_tabulka1.json", "w", encoding="utf-8") as f:
        json.dump(vysledky, f, ensure_ascii=False, indent=2)

    print("\nVýsledky uložené do vysledky_tabulka1.json")
