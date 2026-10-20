"""
Tabuľka 2 – porovnanie triediacich algoritmov

Zadanie:
- RadixSort + jeden z (Bubble, Insert, Select) + jeden z (Quick, Merge, Heap)
  -> v tabuľke 2 sú vybrané: Bubble Sort, Quick Sort, Radix Sort
  (program pre porovnanie meria všetky algoritmy z tabuľky)
- tých istých 5 rôznych dátových sád o veľkosti 10 000 pre všetky algoritmy
- merať čas, počet porovnaní (if, while) a počet presunov dát
- z priemerov odhadnúť priemery pre N = 20 000 (vzorce v Exceli) a porovnať so skutočnosťou

Počet porovnaní = počet vykonaných podmienok (if, while), ktoré porovnávajú triedené hodnoty.
Počet presunov  = počet zápisov prvku dát na nové miesto (výmena dvoch prvkov = 2 presuny).
"""

import json
import random
import time

VELKOSTI_SAD = (10_000, 20_000)
POCET_SAD = 5

# Rovnaký rozsah hodnôt pre obe veľkosti sád -> najväčšie číslo má vždy 5 číslic,
# takže Radix Sort robí pri N = 10 000 aj N = 20 000 rovnaký počet prechodov (d = 5).
MAX_HODNOTA = 99_999


def bubbleSort(unsorted):
    """
    Triedi pole algoritmom Bubble Sort.

    Návratová hodnota:
        tuple: (sorted_arr, comparisons, moves)
    """
    comparisons = 0
    moves = 0

    n = len(unsorted)

    # Opakujeme prechody cez celé pole
    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1

            # Ak sú prvky v nesprávnom poradí, vymeníme ich
            if unsorted[j] > unsorted[j + 1]:
                unsorted[j], unsorted[j + 1] = unsorted[j + 1], unsorted[j]
                moves += 2          # výmena = 2 presunuté prvky

    return unsorted, comparisons, moves


def selectSort(unsorted):
    """
    Triedi pole algoritmom Select Sort (triedenie výberom).

    V každom prechode nájde najmenší prvok nezoradenej časti
    a vymení ho s prvým prvkom nezoradenej časti.

    Návratová hodnota:
        tuple: (sorted_arr, comparisons, moves)
    """
    comparisons = 0
    moves = 0

    n = len(unsorted)

    for i in range(n - 1):
        najmensi = i
        for j in range(i + 1, n):
            comparisons += 1
            if unsorted[j] < unsorted[najmensi]:
                najmensi = j

        if najmensi != i:
            unsorted[i], unsorted[najmensi] = unsorted[najmensi], unsorted[i]
            moves += 2              # výmena = 2 presunuté prvky

    return unsorted, comparisons, moves


def insertSort(unsorted):
    """
    Triedi pole algoritmom Insert Sort (triedenie vkladaním).

    Prvok vyberie z poľa, väčšie prvky pred ním posunie o jedno miesto doprava
    a prvok vloží na uvoľnené miesto.

    Návratová hodnota:
        tuple: (sorted_arr, comparisons, moves)
    """
    comparisons = 0
    moves = 0

    for i in range(1, len(unsorted)):
        kluc = unsorted[i]
        moves += 1                  # prvok vyberieme bokom
        j = i - 1

        comparisons += 1            # každé vyhodnotenie podmienky while
        while j >= 0 and unsorted[j] > kluc:
            unsorted[j + 1] = unsorted[j]
            moves += 1              # posun väčšieho prvku doprava
            j -= 1
            comparisons += 1

        unsorted[j + 1] = kluc
        moves += 1                  # vloženie prvku na správne miesto

    return unsorted, comparisons, moves


def heapSort(unsorted):
    """
    Triedi pole algoritmom Heap Sort (triedenie haldou).

    1. Z poľa vytvorí max-haldu (každý rodič >= svoje deti).
    2. Najväčší prvok (koreň) vymení s posledným prvkom haldy,
       haldu zmenší o 1 a koreň nechá "preosiať" nadol.

    Návratová hodnota:
        tuple: (sorted_arr, comparisons, moves)
    """
    comparisons = 0
    moves = 0

    def preosiat(velkost, i):
        nonlocal comparisons, moves
        while True:
            najvacsi = i
            lavy, pravy = 2 * i + 1, 2 * i + 2

            if lavy < velkost:
                comparisons += 1
                if unsorted[lavy] > unsorted[najvacsi]:
                    najvacsi = lavy
            if pravy < velkost:
                comparisons += 1
                if unsorted[pravy] > unsorted[najvacsi]:
                    najvacsi = pravy

            if najvacsi == i:
                return
            unsorted[i], unsorted[najvacsi] = unsorted[najvacsi], unsorted[i]
            moves += 2
            i = najvacsi

    n = len(unsorted)

    # vytvorenie haldy
    for i in range(n // 2 - 1, -1, -1):
        preosiat(n, i)

    # postupné presúvanie najväčšieho prvku na koniec
    for koniec in range(n - 1, 0, -1):
        unsorted[0], unsorted[koniec] = unsorted[koniec], unsorted[0]
        moves += 2
        preosiat(koniec, 0)

    return unsorted, comparisons, moves


def radixSort(unsorted):
    """
    Triedi pole algoritmom Radix Sort.

    Čísla triedi postupne podľa jednotlivých číslic:
    jednotky, desiatky, stovky a podobne.

    Funguje pre nezáporné celé čísla.

    Návratová hodnota:
        tuple: (sorted_arr, comparisons, moves)
    """
    comparisons = 0
    moves = 0

    if not unsorted:
        return [], comparisons, moves

    # Nájdeme najväčšie číslo v poli (max() porovná n - 1 dvojíc)
    mx = max(unsorted)
    comparisons += len(unsorted) - 1

    # Rad označuje aktuálnu číslicu
    rad = 1

    # Spracúvame číslice, kým najväčšie číslo má danú číslicu
    while mx >= rad:
        comparisons += 1            # podmienka cyklu while

        # Pomocné pole s rovnakou veľkosťou ako pôvodné pole
        result = [0] * len(unsorted)

        # Pole pocty počíta výskyt číslic 0 až 9
        pocty = [0] * 10

        # Zistíme počet výskytov číslic
        for cislo in unsorted:
            cislica = cislo // rad % 10
            pocty[cislica] += 1

        # Vypočítame počiatočné pozície jednotlivých číslic
        pozicie = [0] * 10

        for i in range(1, 10):
            pozicie[i] = pozicie[i - 1] + pocty[i - 1]

        # Umiestnime čísla na správne pozície
        for cislo in unsorted:
            cislica = cislo // rad % 10
            result[pozicie[cislica]] = cislo
            pozicie[cislica] += 1
            moves += 1              # prvok presunutý do pomocného poľa

        # Výsledok použijeme pri ďalšej číslici
        unsorted = result

        # Posunieme sa na ďalšiu číslicu
        rad = rad * 10

    comparisons += 1                # posledná (nesplnená) podmienka while
    return unsorted, comparisons, moves


def quick_sort(arr):
    """
    Triedi pole vzostupne algoritmom Quick Sort (rozdeľuj a panuj).

    Princíp:
        1. Vyberieme pivota (stredný prvok poľa).
        2. Rozdelíme pole na tri časti:
             left   – prvky menšie ako pivot
             middle – prvky rovné pivotu
             right  – prvky väčšie ako pivot
        3. Rekurzívne zotriedime left a right.
        4. Výsledok: _quick_sort(left) + middle + _quick_sort(right)

    Návratová hodnota:
        tuple: (sorted_arr, comparisons, moves)
    """
    comparisons = 0
    moves = 0

    def _quick_sort(a):
        nonlocal comparisons, moves

        if len(a) <= 1:
            return a

        pivot = a[len(a) // 2]

        left, middle, right = [], [], []

        for x in a:
            if x < pivot:
                comparisons += 1
                left.append(x)
            elif x == pivot:
                comparisons += 2
                middle.append(x)
            else:
                comparisons += 2
                right.append(x)
            moves += 1              # prvok presunutý do left / middle / right

        # spojenie častí vytvorí nový zoznam -> každý prvok sa presunie ešte raz
        moves += len(a)
        return _quick_sort(left) + middle + _quick_sort(right)

    return _quick_sort(arr), comparisons, moves


def mergeSort(arr):
    """
    Triedi pole algoritmom Merge Sort (triedenie zlučovaním).

    Pole rozdelí na dve polovice, každú rekurzívne zotriedi
    a obe zoradené polovice zlúči do jedného zoradeného poľa.

    Návratová hodnota:
        tuple: (sorted_arr, comparisons, moves)
    """
    comparisons = 0
    moves = 0

    def _merge_sort(a):
        nonlocal comparisons, moves

        if len(a) <= 1:
            return a

        stred = len(a) // 2
        moves += len(a)             # rozdelenie na polovice skopíruje všetky prvky
        left = _merge_sort(a[:stred])
        right = _merge_sort(a[stred:])

        # zlúčenie dvoch zoradených polovíc
        vysledok = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons += 1
            if left[i] <= right[j]:
                vysledok.append(left[i])
                i += 1
            else:
                vysledok.append(right[j])
                j += 1
            moves += 1

        # zvyšok jednej z polovíc už je zoradený
        vysledok.extend(left[i:])
        vysledok.extend(right[j:])
        moves += (len(left) - i) + (len(right) - j)
        return vysledok

    return _merge_sort(arr), comparisons, moves


# poradie ako v tabuľke 2
ALGORITMY = {
    "Bubble Sort": bubbleSort,
    "Select Sort": selectSort,
    "Insert Sort": insertSort,
    "Heap Sort": heapSort,
    "Quick Sort": quick_sort,
    "Merge Sort": mergeSort,
    "Radix Sort": radixSort,
}


def zmeraj(sort_funkcia, data):
    """Zoradí kópiu dát, vráti (čas v ms, porovnania, presuny)."""
    forSort = data.copy()
    zac = time.perf_counter()
    afterSort, comparisons, moves = sort_funkcia(forSort)
    kon = time.perf_counter()

    assert afterSort == sorted(data), "zoznam nie je správne zoradený"
    return (kon - zac) * 1000, comparisons, moves


if __name__ == "__main__":
    vysledky = {}

    for n in VELKOSTI_SAD:
        vysledky[n] = {nazov: [] for nazov in ALGORITMY}

        for j in range(POCET_SAD):
            # tá istá dátová sada pre všetky tri algoritmy
            zoznam = [random.randint(0, MAX_HODNOTA) for _ in range(n)]

            print(f"\nN = {n}, sada {j + 1}")
            for nazov, funkcia in ALGORITMY.items():
                cas_ms, comparisons, moves = zmeraj(funkcia, zoznam)
                vysledky[n][nazov].append({"cas_ms": cas_ms, "porovnania": comparisons, "presuny": moves})
                print(f"  {nazov:12} čas: {cas_ms:12.3f} ms   porovnania: {comparisons:12}   presuny: {moves:12}")

    with open("vysledky_tabulka2.json", "w", encoding="utf-8") as f:
        json.dump(vysledky, f, ensure_ascii=False, indent=2)

    print("\nVýsledky uložené do vysledky_tabulka2.json")
