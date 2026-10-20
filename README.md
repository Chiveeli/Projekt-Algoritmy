# Projekt: Algoritmy a ich zložitosť


## Súbory projektu

| Súbor | Obsah |
|---|---|
| `LinearAndBinarySearch.py` | Linear Search a Binary Search – meranie pre tabuľku 1 |
| `Sorty.py` | triediace algoritmy a meranie pre tabuľku 2 (v tabuľke sú podľa zadania Bubble, Quick a Radix Sort) |
| `JazdecDFS.py`, `JazdecBFS.py` | Jazdec na šachovnici – prehľadávanie do hĺbky a do šírky (tabuľka 3) |
| `FloodFill.py` | interaktívny Flood Fill v Pygame (BFS, DFS, DFS rekurzívne) |
| `FloodFillMeranie.py` | meranie Flood Fill bez okna a bez animácie (tabuľka 3) |
| `analyza algoritmov Elizabeth Blascakova.xlsx` | tabuľky 1–3 s meraniami, vzorcami pre priemery a odhady a hárok Grafy |

```
python LinearAndBinarySearch.py
python Sorty.py
python JazdecDFS.py 120              # limit 120 s na jeden beh
python JazdecBFS.py 120 15000000     # limit 120 s alebo 15 miliónov ciest v pamäti
python FloodFillMeranie.py
python FloodFill.py                  # okno s kreslením a plechovkou (pip install pygame)
```

Každý merací skript vypíše výsledky a uloží ich do súboru `vysledky_*.json`.

---

## 1. Teória

### Rekurzia v programovaní

Rekurzia je spôsob riešenia problému, pri ktorom funkcia volá samu seba. Každé ďalšie volanie rieši menšiu časť
pôvodného problému, až kým sa nedosiahne základný prípad, ktorý volanie ukončí.

```python
def faktorial(n):
    if n <= 1:                      # základný prípad – ukončí rekurziu
        return 1
    return n * faktorial(n - 1)     # funkcia volá samu seba s menším n
```

Rekurzia je použitá napríklad v Quick Sorte, v Jazdcovi (DFS s backtrackingom) a vo Flood Fill DFS
rekurzívne. Python predvolene dovolí len približne 1000 vnorených volaní, preto pri veľkej hĺbke treba limit zvýšiť
(`sys.setrecursionlimit`).

### Zložitosť algoritmu

Zložitosť algoritmu vyjadruje, ako sa mení čas vykonania alebo spotreba pamäte pri zväčšovaní vstupných údajov.
Používa sa Big O notácia:

- O(1) – konštantná zložitosť
- O(log n) – logaritmická zložitosť
- O(n) – lineárna zložitosť
- O(n·log n) – linearitmická zložitosť (Heap Sort, Merge Sort, Quick Sort v priemere)
- O(n²) – kvadratická zložitosť
- O(n³) – kubická zložitosť
- O(2ⁿ) – exponenciálna zložitosť (napr. vyskúšanie všetkých podmnožín)

### Príklady časovej zložitosti

**O(1) – konštantná zložitosť**
Algoritmus vykoná rovnaký počet operácií bez ohľadu na veľkosť vstupu.
Príklad: získanie prvku poľa podľa indexu.

```python
def prvy_prvok(zoznam):
    return zoznam[0]
```

**O(log n) – logaritmická zložitosť**
Pri každom kroku sa veľkosť problému zmenší, napríklad na polovicu.
Príklad: Binárne vyhľadávanie – Binary Search.

```python
def pocet_deleni_dvomi(n):
    kroky = 0
    while n > 1:
        n = n // 2                  # problém sa zmenší na polovicu
        kroky += 1
    return kroky
```

**O(n) – lineárna zložitosť**
Algoritmus spracuje každý prvok najviac raz.
Príklad: Lineárne vyhľadávanie – Linear Search.

```python
def sucet(zoznam):
    s = 0
    for x in zoznam:                # jeden prechod cez všetky prvky
        s += x
    return s
```

**O(n²) – kvadratická zložitosť**
Algoritmus používa často dva vnorené cykly.
Príklad: Bublinové triedenie – Bubble Sort.

```python
def pocet_rovnakych_dvojic(zoznam):
    pocet = 0
    for i in range(len(zoznam)):
        for j in range(i + 1, len(zoznam)):     # každá dvojica prvkov
            if zoznam[i] == zoznam[j]:
                pocet += 1
    return pocet
```

**O(n³) – kubická zložitosť**
Algoritmus používa napríklad tri vnorené cykly.
Príklad: porovnávanie všetkých trojíc prvkov alebo niektoré operácie s maticami.

```python
def nasob_matice(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):                  # tri vnorené cykly
                C[i][j] += A[i][k] * B[k][j]
    return C
```

### Riešenie úloh z pracovného listu

#### Test

1. A) O(1)
2. D) O(log n)
3. A) O(n²)
4. D) O(n²)
5. C) O(2ⁿ)
6. B) O(n²)
7. A) O(n log n)
8. D) O(n²)
9. B) log₂ n
10. C) 4×
11. D) O(n² + n) = O(n²)
12. B) O(n)

#### Úlohy na precvičenie – odhad času

| Úloha | Výsledok |
|---|---|
| 1 | 6 sekúnd |
| 2 | 36 sekúnd |
| 3 | 32 sekúnd |
| 4 | 48 ms |
| 5 | 16 sekúnd |
| 6 | 120 000 000 prvkov |
| 7 | O(n³) |
| 8 | O(n²) |
| 9 | O(n) |
| 10 | O(n³) |
| 11 | 10 000 prvkov |
| 12 | O(2ⁿ) |

### Opis algoritmov

#### Lineárne vyhľadávanie – Linear Search

Lineárne vyhľadávanie prechádza prvky postupne od začiatku po koniec, až kým nenájde hľadanú hodnotu alebo nepríde
na koniec zoznamu.

- Použitie: hľadanie v malých alebo nezoradených zoznamoch a pri jednorazovom hľadaní, keď sa neoplatí zoznam
  najprv zoraďovať
- Časová zložitosť: O(n)
- Pamäťová zložitosť: O(1)
- Požiadavka na vstup: zoznam nemusí byť zoradený
- Výhoda: jednoduchá implementácia
- Nevýhoda: pri veľkých zoznamoch môže byť pomalé

#### Binárne vyhľadávanie – Binary Search

Binárne vyhľadávanie porovnáva hľadanú hodnotu so stredným prvkom zoznamu. Podľa výsledku porovnania pokračuje
iba v ľavej alebo pravej polovici zoznamu.

- Použitie: rýchle hľadanie vo veľkých zoradených dátach, napríklad v slovníku, telefónnom zozname alebo
  v indexoch databáz
- Časová zložitosť: O(log n)
- Pamäťová zložitosť: O(1)
- Požiadavka na vstup: zoznam musí byť zoradený
- Výhoda: veľmi rýchle vyhľadávanie
- Nevýhoda: nedá sa priamo použiť na neusporiadaný zoznam

#### Jazdec na šachovnici – DFS/BFS

Pri tejto úlohe hľadáme cestu jazdca po šachovnici. Šachovnicu môžeme znázorniť ako graf, v ktorom každé pole
predstavuje vrchol a možný pohyb jazdca predstavuje hranu. Hľadáme cestu, pri ktorej jazdec navštívi každé pole
práve raz.

- Použitie: DFS a BFS slúžia na prehľadávanie grafov a všetkých možností – hľadanie cesty v bludisku alebo na mape,
  riešenie hlavolamov a hier; BFS nájde cestu s najmenším počtom krokov
- Požiadavka na vstup: veľkosť šachovnice n × n a štartové pole (x, y) na šachovnici; jazdec sa pohybuje do tvaru „L“
  a každé pole môže navštíviť len raz

**Prehľadávanie do hĺbky – Depth-First Search, DFS**
DFS postupuje čo najďalej jedným smerom. Keď už nemôže pokračovať, vráti sa späť (backtracking) a skúsi inú možnosť.

- Používa zásobník alebo rekurziu
- Vhodné na úplné prehľadanie možností
- Pri obyčajnom prehľadaní grafu (každý vrchol navštívime raz): časová zložitosť O(V + E), pamäťová O(V)

**Prehľadávanie do šírky – Breadth-First Search, BFS**
BFS najskôr preskúma všetky polia dostupné na jeden krok, potom všetky polia dostupné na dva kroky a podobne.

- Používa klony (agentov) – každá rozpracovaná cesta je jeden agent, ktorý sa v ďalšom kroku rozdelí na nových agentov
- Vhodné na hľadanie najkratšej cesty
- Pri obyčajnom prehľadaní grafu: časová zložitosť O(V + E), pamäťová O(V)

**Zložitosť pri hľadaní cesty jazdca**
Pri hľadaní cesty cez všetky polia sa neprehľadávajú len vrcholy, ale všetky možné cesty – to isté pole sa objaví
v obrovskom počte rôznych ciest. Z každého z n² polí môže jazdec skúsiť až 8 ťahov, preto je horný odhad zložitosti
**O(8^(n²))** (exponenciálna). Pamäť: DFS si pamätá len jednu rozpracovanú cestu – O(n²); BFS si musí pamätať
všetky cesty jednej úrovne naraz, takže jeho pamäť rastie tiež exponenciálne.

#### Bublinové triedenie – Bubble Sort

Bublinové triedenie porovnáva susedné prvky a vymieňa ich, ak sú v nesprávnom poradí. Väčšie prvky sa postupne
presúvajú na koniec zoznamu, podobne ako bubliny stúpajú nahor. Algoritmus opakuje prechody zoznamom dovtedy, kým sa
nevykoná žiadna výmena. (Verzia v `Sorty.py` robí vždy všetky prechody, preto má vždy presne n·(n − 1)/2 porovnaní.)

- Použitie: výučba triedenia a triedenie veľmi malých zoznamov
- Časová zložitosť: O(n²)
- Pamäťová zložitosť: O(1)
- Požiadavka na vstup: ľubovoľné pole alebo zoznam
- Výhoda: jednoduchý na pochopenie a implementáciu
- Nevýhoda: pomalý pri veľkom počte prvkov

#### Rýchle triedenie – Quick Sort

Rýchle triedenie vyberie jeden prvok ako pivot. Ostatné prvky rozdelí na menšie a väčšie ako pivot. Následne
rovnakým spôsobom rekurzívne zoradí obe časti.

- Použitie: bežné triedenie veľkých dát v praxi, je základom triedenia v mnohých knižniciach (napr. v C++ a Jave)
- Časová zložitosť: O(n·log n) v priemere, O(n²) v najhoršom prípade
- Pamäťová zložitosť: približne O(log n) pri triedení priamo v poli; verzia v `Sorty.py` vytvára nové zoznamy
  (left, middle, right), preto potrebuje O(n)
- Požiadavka na vstup: ľubovoľné pole alebo zoznam
- Výhoda: veľmi rýchly v praxi a nevyžaduje veľké pomocné pole
- Nevýhoda: pri nevhodnom výbere pivota môže byť výrazne pomalší

#### Radix Sort – triedenie podľa číslic

Radix Sort triedi čísla postupne podľa jednotlivých číslic, od poslednej po prvú (jednotky, desiatky, stovky…).
n predstavuje počet prvkov a d počet číslic najväčšieho čísla.

- Použitie: triedenie veľkého množstva celých čísel alebo kľúčov rovnakej dĺžky – PSČ, telefónne čísla,
  identifikačné čísla, dátumy
- Časová zložitosť: O(n·d)
- Pamäťová zložitosť: O(n)
- Požiadavka na vstup: najčastejšie celé čísla (verzia v `Sorty.py` nezáporné celé čísla)
- Výhoda: rýchly pri veľkom počte čísel s podobným počtom číslic, prvky medzi sebou vôbec neporovnáva
- Nevýhoda: potrebuje pomocnú pamäť a nie je vhodný pre všetky typy údajov

#### Flood Fill – BFS a DFS

Flood Fill vyfarbí súvislú oblasť rovnakej farby, v ktorej leží zvolený bod – ako „plechovka“ v grafických
editoroch. Obrázok je graf: každý pixel je vrchol a susedné pixely (4-susedstvo: hore, dole, vľavo, vpravo;
8-susedstvo aj šikmo) sú spojené hranou. Algoritmus prefarbí štartovací pixel, potom všetkých jeho susedov s pôvodnou
farbou, potom ich susedov atď.

- Použitie: „plechovka“ v grafických editoroch, vyfarbovanie oblastí na mapách, hry (napr. odkrytie prázdnych polí
  v Míny / Minesweeper), hľadanie súvislých oblastí v obrázku
- **Flood Fill BFS** – čakajúce pixely sú vo fronte (`deque`, berie sa zo začiatku `popleft`) → farba sa šíri ako vlna
  na všetky strany rovnomerne
- **Flood Fill DFS** – čakajúce pixely sú v zásobníku (berie sa z konca `pop`) → farba sa šíri ako „had“ do hĺbky
- **Flood Fill DFS rekurzívne** – funkcia zavolá samu seba pre všetkých susedov; zápis je najkratší, ale hĺbka
  rekurzie môže byť až počet pixelov, preto treba zvýšiť limit rekurzie a spustiť ju vo vlákne s väčším zásobníkom
- Časová zložitosť: O(n), kde n je počet prefarbených pixelov (každý pixel sa prefarbí raz a skontrolujú sa jeho
  4 alebo 8 susedia)
- Pamäťová zložitosť: O(n) – front, zásobník alebo zásobník volaní
- Požiadavka na vstup: obrázok (mriežka pixelov), štartovací bod a nová farba; oblasť má byť uzavretá, inak sa
  vyfarbí aj okolie
- Výhoda: jednoduchý a lineárny
- Nevýhoda: pri veľkých plochách potrebuje veľa pomocnej pamäte, rekurzívna verzia bez zvýšeného limitu skončí
  chybou `RecursionError`

---

## 2. Praktická časť – merania

- Tabuľka 1: zoradený zoznam sa generuje rovno zoradený (krok 0 – 9, takže vznikajú opakované čísla aj medzery).
  10 hľadaných hodnôt je náhodných z celého rozsahu ⟨min, max⟩, rovnakých pre LS aj BS; generujú sa znova, kým
  nie je nájdených 1 až 5 hodnôt. N1 = 10 000 000 (rozsah 3 – 45 005 181), N2 = 100 000 000 (rozsah 4 – 449 998 473).
- Tabuľka 2: podľa zadania Radix Sort, Bubble Sort (z Bubble / Insert / Select) a Quick Sort (z Quick / Merge / Heap);
  5 náhodných sád s hodnotami 0 – 99 999, tie isté pre všetky algoritmy, veľkosti 10 000 a 20 000.
  Porovnania = vykonané podmienky (if, while), ktoré porovnávajú triedené hodnoty; presuny = zápisy prvku na nové
  miesto (výmena = 2 presuny).
- Tabuľka 3: Jazdec s limitom 120 s (DFS) a 120 s alebo 15 miliónov ciest v pamäti (BFS); Flood Fill bez animácie
  na 4 útvaroch na plátne 900 × 576 px.
- Anomália: čas (prepočítaný na 1 porovnanie alebo pixel) väčší ako 2 × medián sady → bunka je v Exceli červená a
  nezapočíta sa do priemeru.
- Odhady v Exceli sú vzorce z priemerov menšej sady: O(n) · N2/N1, O(log n) · log₂N2/log₂N1, O(n²) · (N2/N1)²,
  O(n·log n) · (N2·log₂N2)/(N1·log₂N1), Jazdec · 8^(n² − 4²).

### Tabuľka 1 – Linear Search vs Binary Search

| | LS čas (ms) | LS porovnania | BS čas (ms) | BS porovnania |
|---|---:|---:|---:|---:|
| N1 = 10 000 000 – priemer | 126,773 | 8 226 390,5 | 0,0048 | 46,0 |
| N2 = 100 000 000 – odhad | 1 267,727 | 82 263 905 | 0,0055 | 52,6 |
| N2 = 100 000 000 – skutočnosť | 2 130,614 | 96 884 327,6 | 0,0358 | 53,1 |
| **odhad / skutočnosť** | **59,5 %** | **84,9 %** | **15,3 %** | **99,0 %** |

Nájdené / nenájdené hodnoty: N1 2 / 8, N2 1 / 9.

### Tabuľka 2 – triedenie (priemery z 5 sád)

| Algoritmus | Zložitosť | čas N = 10 000 (ms) | čas N = 20 000 odhad (ms) | čas N = 20 000 skutočnosť (ms) | odhad / skut. čas | porovnania | presuny |
|---|---|---:|---:|---:|---:|---:|---:|
| Bubble Sort | O(n²) | 1 729,712 | 6 918,849 | 6 992,221 | 99,0 % | 100,0 % | 99,7 % |
| Quick Sort | O(n·log n) | 6,088 | 13,091 | 12,867 | 101,7 % | 98,8 % | 99,3 % |
| Radix Sort | O(d·n) | 3,819 | 7,639 | 7,730 | 98,8 % | 100,0 % | 100,0 % |

### Tabuľka 3 – Jazdec na šachovnici

| n | štart | DFS cesty | DFS čas (ms) | BFS cesty | BFS čas (ms) |
|---|---|---:|---:|---:|---:|
| 4 | 0,0 | 17 784 (cesta neexistuje) | 1,8 | 17 784 | 1,5 |
| 4 | 1,0 | 15 080 (cesta neexistuje) | 1,5 | 15 080 | 1,1 |
| 4 | 1,1 | 12 008 (cesta neexistuje) | 1,1 | 12 008 | 0,9 |
| 5 | 0,0 | 410 528 | 49,3 | 13 878 200 | 1 659,9 |
| 5 | 1,0 | 14 635 368 (cesta neexistuje) | 1 685,1 | 14 635 368 | 1 721,3 |
| 5 | 2,1 | 8 231 144 (cesta neexistuje) | 929,2 | 8 231 144 | 995,6 |
| 6 | 0,0 | 1 277 366 | 203,9 | ≥ 115 000 000 (pamäť) | ≥ 18 414 |
| 6 | 1,0 | ≥ 756 000 019 (limit 120 s) | ≥ 120 143 | ≥ 81 000 000 (pamäť) | ≥ 11 692 |
| 7 | 0,0 | 593 781 | 129,4 | ≥ 75 000 000 (pamäť) | ≥ 13 045 |
| 8 | 0,0 | ≥ 412 000 011 (limit 120 s) | ≥ 120 096 | ≥ 54 000 000 (pamäť) | ≥ 9 415 |

(Výber riadkov – všetky štarty sú v Exceli.) Odhad O(8^(n²)) je napríklad pre n = 5 a štart 0,0 až 2,39·10¹²
skúmaných ciest a pre n = 8 až 3,97·10⁴⁷.

### Tabuľka 3 – Flood Fill

| Útvar | pixely | BFS (ms) | odhad / skut. | DFS R (ms) | odhad / skut. | DFS (ms) | odhad / skut. |
|---|---:|---:|---:|---:|---:|---:|---:|
| štvorec 100 × 100 | 8 836 | 3,869 | základ | 4,491 | základ | 3,791 | základ |
| kruh r = 150 | 67 800 | 31,425 | 94,5 % | 34,446 | 100,0 % | 32,166 | 90,4 % |
| trojuholník 700 × 450 | 155 109 | 71,692 | 94,7 % | 78,457 | 100,5 % | 74,133 | 89,8 % |
| obdĺžnik 880 × 556 | 480 700 | 242,156 | 86,9 % | 241,010 | 101,4 % | 229,270 | 90,0 % |

---

## 3. Vyhodnotenie praktickej časti

> Praktickú časť vyhodnoťte – ako vnímate výhody, nevýhody algoritmov, či sa naplnili očakávania z odhadov, či
> vznikali anomálie a prečo asi, čo ste sa pri spracovávaní projektu naučili, v čom zdokonalili.

Binary Search bol oveľa rýchlejší ako Linear Search, ale potrebuje zoradený zoznam. Bubble Sort bol pri veľkých dátach pomalý, Quick Sort rýchly a Radix Sort najrýchlejší, hoci vie triediť len celé čísla. Odhady pri triedení sa naplnili takmer presne, na 98 až 102 %. Pri Binary Search sedel odhad porovnaní, ale časy boli vyššie, lebo veľký zoznam zaberal veľa pamäte. Pri Jazdcovi bol odhad oveľa vyšší ako skutočnosť, no exponenciálny rast sa potvrdil. DFS bol na Jazdca lepší ako BFS, ktorý pri n = 6 prekročil limit pamäte. Flood Fill bol vo všetkých verziách lineárny a odhad sa naplnil. Anomáliu som mala len pri prvom binárnom vyhľadávaní, asi preto, že dáta ešte neboli v rýchlej pamäti procesora.

Naučila som sa, že zložitosť ukazuje, ako rastie práca, nie presný čas. Zdokonalila som sa v Pythone, v meraní algoritmov a v práci s Excelom.
