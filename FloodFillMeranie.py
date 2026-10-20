"""
Tabuľka 3 – meranie Flood Fill bez okna a bez animácie

Každý uzavretý útvar sa nakreslí na čisté plátno (rovnaké ako v FloodFill.py)
a vyplní sa algoritmami BFS, DFS (zásobník) aj DFS R (rekurzia), susedstvo 4.
Zaznamená sa počet prefarbených pixelov a čas vypĺňania v ms.
"""
import json
import os
import time

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")   # bez otvárania okna

import pygame

from FloodFill import BIELA, CIERNA, HRUBKA, PANEL, PALETA, SIRKA, VYSKA, flood_fill, flood_fill_rekurzivne

# názov, kreslenie obrysu, bod vnútri útvaru
UTVARY = [
    ("štvorec 100×100",
     lambda p: pygame.draw.rect(p, CIERNA, (40, 40, 100, 100), HRUBKA), (90, 90)),
    ("kruh r = 150",
     lambda p: pygame.draw.circle(p, CIERNA, (450, 288), 150, HRUBKA), (450, 288)),
    ("trojuholník 700×450",
     lambda p: pygame.draw.polygon(p, CIERNA, [(100, 510), (800, 510), (450, 60)], HRUBKA), (450, 400)),
    ("obdĺžnik 880×556",
     lambda p: pygame.draw.rect(p, CIERNA, (10, 10, 880, 556), HRUBKA), (450, 288)),
]

ALGORITMY = ["BFS", "DFS R", "DFS"]


def nove_platno(kresli):
    platno = pygame.Surface((SIRKA, VYSKA - PANEL))
    platno.fill(BIELA)
    kresli(platno)
    return platno


def vypln(platno, start, algoritmus):
    """Vyplní útvar bez animácie, vráti (počet pixelov, čas v ms)."""
    farba = PALETA[1]
    platno.lock()
    zac = time.perf_counter()
    if algoritmus == "DFS R":
        pocet = flood_fill_rekurzivne(platno, start, farba)
    else:
        pocet = 0
        for pocet in flood_fill(platno, start, farba, algoritmus, 4):
            pass
    cas_ms = (time.perf_counter() - zac) * 1000
    platno.unlock()
    return pocet, cas_ms


if __name__ == "__main__":
    pygame.init()

    # zahrievacie kolo (prvé volania funkcií), nezapisuje sa
    for algoritmus in ALGORITMY:
        vypln(nove_platno(UTVARY[0][1]), UTVARY[0][2], algoritmus)

    vysledky = []
    for algoritmus in ALGORITMY:
        for nazov, kresli, start in UTVARY:
            pocet, cas_ms = vypln(nove_platno(kresli), start, algoritmus)
            print(f"{algoritmus:6} {nazov:22} {pocet:8} px {cas_ms:10.3f} ms")
            vysledky.append({"algoritmus": algoritmus, "utvar": nazov, "pixely": pocet, "cas_ms": cas_ms})

    with open("vysledky_floodfill.json", "w", encoding="utf-8") as f:
        json.dump(vysledky, f, ensure_ascii=False, indent=2)

    pygame.quit()
