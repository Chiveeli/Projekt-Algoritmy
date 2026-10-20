"""
Jazdec na šachovnici – prehľadávanie do hĺbky (DFS) s backtrackingom

Počet skúmaných ciest = stepcnt = počet vyskúšaných ťahov jazdcom.
Zložitosť O(8^(n*n)) – z každého z n*n políčok skúšame až 8 ťahov.
"""
import json
import sys
import time

TAHY = ((2, 1), (1, 2), (-1, 2), (-2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1))


class PrekrocenyLimit(Exception):
    pass


def dfs(ax, ay):
    global stepcnt, visited, dalsia_kontrola
    visited += ((ax, ay),)
#   print(visited)
    if len(visited) == n * n: return True
    for dx, dy in TAHY:
        stepcnt += 1
        nx, ny = ax + dx, ay + dy
        if 0 <= nx < n and 0 <= ny < n:
            if (nx, ny) in visited: continue
            elif dfs(nx, ny) == True: return True
    visited = visited[:-1]            # backtracking
    if stepcnt >= dalsia_kontrola:    # raz za milión krokov skontrolujeme časový limit
        dalsia_kontrola += 1_000_000
        if koniec is not None and time.perf_counter() > koniec:
            raise PrekrocenyLimit
    return False


def jazdec_dfs(velkost, x, y, limit_s=None):
    """
    Vráti (našiel_cestu, cesta, počet skúmaných ciest, čas v ms, dokončené).
    Ak beh prekročí limit_s sekúnd, preruší sa a dokončené = False.
    """
    global n, visited, stepcnt, koniec, dalsia_kontrola
    n = velkost
    visited = ()
    stepcnt = 0
    dalsia_kontrola = 1_000_000

    zac = time.perf_counter()
    koniec = zac + limit_s if limit_s else None
    try:
        nasiel, dokoncene = dfs(x, y), True
    except PrekrocenyLimit:
        nasiel, dokoncene = None, False
    cas_ms = (time.perf_counter() - zac) * 1000
    return nasiel, visited, stepcnt, cas_ms, dokoncene


# štartovacie pozície z tabuľky 3
STARTY = [(4, 0, 0), (4, 1, 0), (4, 1, 1),
          (5, 0, 0), (5, 1, 0), (5, 2, 0), (5, 1, 1), (5, 2, 1), (5, 2, 2),
          (6, 0, 0), (6, 1, 0), (6, 2, 0), (6, 1, 1), (6, 2, 1), (6, 2, 2),
          (7, 0, 0), (8, 0, 0)]

if __name__ == "__main__":
    # python JazdecDFS.py [limit v sekundách pre jeden beh]
    limit_s = float(sys.argv[1]) if len(sys.argv) > 1 else 600
    vysledky = []

    for velkost, x, y in STARTY:
        nasiel, cesta, kroky, cas_ms, dokoncene = jazdec_dfs(velkost, x, y, limit_s)
        stav = nasiel if dokoncene else f"prerušené po {limit_s:.0f} s"
        print(f"n = {velkost}  x,y = ({x},{y})  {stav}  {kroky:15_} ciest  {cas_ms:14.3f} ms".replace("_", " "))
        vysledky.append({"n": velkost, "x": x, "y": y, "nasiel": nasiel, "kroky": kroky,
                         "cas_ms": cas_ms, "dokoncene": dokoncene, "limit_s": limit_s})

    with open("vysledky_jazdec_dfs.json", "w", encoding="utf-8") as f:
        json.dump(vysledky, f, ensure_ascii=False, indent=2)

#   Jazdec na sachovnici (počet skúmaných ciest, merané JazdecDFS.py, limit 120 s)
#   n = 4    x,y = (0,0)    False         17 784
#   n = 4    x,y = (1,0)    False         15 080
#   n = 4    x,y = (1,1)    False         12 008

#   n = 5    x,y = (0,0)    True         410 528
#   n = 5    x,y = (1,0)    False     14 635 368   (5x5: z políčka s nepárnym x+y cesta neexistuje)
#   n = 5    x,y = (2,0)    True         310 629
#   n = 5    x,y = (1,1)    True       5 019 640
#   n = 5    x,y = (2,1)    False      8 231 144
#   n = 5    x,y = (2,2)    True         283 713

#   n = 6    x,y = (0,0)    True       1 277 366
#   n = 6    x,y = (1,0)    prerušené po 120 s (> 756 000 000)
#   n = 6    x,y = (2,0)    True         205 620
#   n = 6    x,y = (1,1)    True      14 288 574
#   n = 6    x,y = (2,1)    prerušené po 120 s (> 783 000 000)
#   n = 6    x,y = (2,2)    True       5 365 424
#   n = 7    x,y = (0,0)    True         593 781
#   n = 8    x,y = (0,0)    prerušené po 120 s (> 412 000 000)

#   Zlozitost O(8^(n*n))
