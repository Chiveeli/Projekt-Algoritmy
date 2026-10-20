"""
Flood fill (vyplnenie plochy) v Pygame
=====================================

Režim KRESBA:     ťahaj myšou so stlačeným ľavým tlačidlom a čmáraj súvislé čiary.
Režim PLECHOVKA:  klikni dovnútra uzavretej oblasti a vyplní sa farbou.

Ovládanie:
  K           režim kresba
  P           režim plechovka
  Medzerník   prepnutie medzi kresbou a plechovkou
  B           prepnutie algoritmu BFS (front) / DFS (zásobník) / DFS R (rekurzia)
  N           prepnutie susedstva 4 / 8
  A           animácia zapnutá / vypnutá
  šípky ↑ ↓   rýchlosť animácie
  1 – 6       farba výplne
  C           vymazanie plátna
  Esc         koniec

Pri vypnutej animácii (a vždy pri DFS R) sa v paneli zobrazí čas vypĺňania v ms.
Merania pre tabuľku 3 bez okna: python FloodFillMeranie.py

Inštalácia:  pip install pygame
"""
import sys
import threading
import time
from collections import deque

import pygame

# ---------- nastavenia ----------
SIRKA, VYSKA = 900, 640        # veľkosť okna
PANEL = 64                     # výška horného panela s informáciami
HRUBKA = 3                     # hrúbka čiary pri kreslení

BIELA = (255, 255, 255)
CIERNA = (20, 20, 20)
PALETA = [
    (231, 76, 60),    # 1 červená
    (46, 134, 222),   # 2 modrá
    (39, 174, 96),    # 3 zelená
    (241, 196, 15),   # 4 žltá
    (155, 89, 182),   # 5 fialová
    (230, 126, 34),   # 6 oranžová
]

# smery pohybu k susedom
SUSEDIA_4 = [(1, 0), (0, 1),(-1, 0), (0, -1)]
SUSEDIA_8 = SUSEDIA_4 + [(1, 1), (1, -1), (-1, 1), (-1, -1)]


# ---------- algoritmus ----------
# rekurzívna verzia (krátka, ale pre veľké plochy by spadla
# na RecursionError – Python predvolene dovolí len cca 1000 vnorených volaní),
# preto zvýšime limit rekurzie a spúšťame ju vo vlákne s veľkým zásobníkom.
sys.setrecursionlimit(10**6)
threading.stack_size(256 * 512 * 512)   # 64 MB zásobník pre vlákno s rekurziou


def flood_fill_rekurzivneDFS(platno, x, y, stara, nova):
    """Vráti počet prefarbených pixelov (susedstvo 4)."""
    if not (0 <= x < platno.get_width() and 0 <= y < platno.get_height()):
        return 0
    if platno.get_at((x, y)) != stara:
        return 0
    platno.set_at((x, y), nova)
    return (1 + flood_fill_rekurzivneDFS(platno, x + 1, y, stara, nova)
              + flood_fill_rekurzivneDFS(platno, x, y + 1, stara, nova)
              + flood_fill_rekurzivneDFS(platno, x - 1, y, stara, nova)
              + flood_fill_rekurzivneDFS(platno, x, y - 1, stara, nova))


def flood_fill_rekurzivne(platno, start, nova_farba):
    """Spustí rekurzívne DFS vo vlákne s veľkým zásobníkom, vráti počet prefarbených pixelov."""
    stara_farba = platno.get_at(start)
    if stara_farba == nova_farba:
        return 0

    # rekurziu spustíme PRED prefarbením štartu a s PÔVODNOU farbou
    vysledok = [0]

    def uloha():
        vysledok[0] = flood_fill_rekurzivneDFS(platno, start[0], start[1], stara_farba, nova_farba)

    vlakno = threading.Thread(target=uloha)
    vlakno.start()
    vlakno.join()
    return vysledok[0]


def flood_fill(platno, start, nova_farba, algoritmus="BFS", susedstvo=4):
# Vyplní súvislú oblasť rovnakej farby, v ktorej leží bod start.
#
# Je to generátor: po spracovaní každého pixelu vráti (yield) počet
# doteraz spracovaných pixelov. Vďaka tomu môžeme vypĺňanie animovať.
#
# BFS -> berieme prvky zo začiatku frontu  (popleft) -> šíri sa ako vlna
# DFS -> berieme prvky z konca (zásobník)  (pop) -> "had" do hĺbky
# (rekurzívne DFS je vo funkcii flood_fill_rekurzivne)
    sirka, vyska = platno.get_size()
    stara_farba = platno.get_at(start)

    if stara_farba == nova_farba:
        return

    smery = SUSEDIA_4 if susedstvo == 4 else SUSEDIA_8
    cakajuce = deque([start])
    platno.set_at(start, nova_farba)
    spracovane = 0

    while cakajuce:
        if algoritmus == "DFS": x,y = cakajuce.pop()
        else: x, y = cakajuce.popleft()      # BFS
        spracovane += 1
        for dx, dy in smery:
            nx, ny = x + dx, y + dy
            if 0 <= nx < sirka and 0 <= ny < vyska and platno.get_at((nx, ny)) == stara_farba:
                platno.set_at((nx, ny), nova_farba)
                cakajuce.append((nx, ny))
        yield spracovane               # vo vnútri cyklu -> animácia funguje


# ---------- pomocné funkcie ----------
def na_platno(pozicia):
    """Prepočet súradníc okna na súradnice plátna (pod panelom)."""
    x, y = pozicia
    return x, y - PANEL


def je_na_platne(pozicia):
    x, y = pozicia
    return 0 <= x < SIRKA and PANEL <= y < VYSKA


def kresli_panel(okno, font, stav):
    pygame.draw.rect(okno, (40, 44, 52), (0, 0, SIRKA, PANEL))

    rezim = "KRESBA" if stav["rezim"] == "kresba" else "PLECHOVKA"
    animacia = f"zap ({stav['rychlost']} px/snímka)" if stav["animacia"] else "vyp"
    riadok1 = (f"Režim: {rezim}   |   Algoritmus: {stav['algoritmus']}   |   "
               f"Susedstvo: {stav['susedstvo']}   |   Animácia: {animacia}")
    riadok2 = ("K/P/medzera režim   B algoritmus   N susedstvo   A animácia   "
               "↑↓ rýchlosť   1–6 farba   C vymazať")

    okno.blit(font.render(riadok1, True, (240, 240, 240)), (12, 8))
    okno.blit(font.render(riadok2, True, (160, 166, 178)), (12, 36))

    # aktuálna farba výplne
    pygame.draw.rect(okno, stav["farba"], (SIRKA - 52, 12, 40, 40), border_radius=6)
    pygame.draw.rect(okno, (240, 240, 240), (SIRKA - 52, 12, 40, 40), 2, border_radius=6)

    # počet spracovaných pixelov (a čas bez animácie) pri poslednom vypĺňaní
    if stav["pocet"]:
        info = f"{stav['pocet']} px"
        if stav["cas_ms"] is not None:
            info += f"  {stav['cas_ms']:.1f} ms"
        text = font.render(info, True, (240, 196, 120))
        okno.blit(text, (SIRKA - 64 - text.get_width(), 22))


def nastav_kurzor(rezim):
    try:
        if rezim == "kresba":
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
    except (AttributeError, pygame.error):
        pass  # staršie verzie Pygame systémové kurzory nepoznajú


# ---------- hlavný program ----------
ALGORITMY = ["BFS", "DFS", "DFS R"]


def main():
    pygame.init()
    okno = pygame.display.set_mode((SIRKA, VYSKA))
    pygame.display.set_caption("Flood fill – čmáranica a plechovka")
    hodiny = pygame.time.Clock()
    font = pygame.font.SysFont("dejavusans,arial,freesans", 18)

    platno = pygame.Surface((SIRKA, VYSKA - PANEL))
    platno.fill(BIELA)

    stav = {
        "rezim": "kresba",
        "algoritmus": "BFS",
        "susedstvo": 4,
        "animacia": True,
        "rychlost": 1500,      # koľko pixelov sa spracuje za jednu snímku
        "farba": PALETA[0],
        "pocet": 0,
        "cas_ms": None,        # čas posledného vypĺňania bez animácie
    }

    kreslim = False
    posledny_bod = None
    vyplnanie = None           # bežiaci generátor flood_fill (počas animácie)

    nastav_kurzor(stav["rezim"])
    bezi = True
    while bezi:
        for udalost in pygame.event.get():
            if udalost.type == pygame.QUIT:
                bezi = False

            elif udalost.type == pygame.KEYDOWN:
                k = udalost.key
                if k == pygame.K_ESCAPE:
                    bezi = False
                elif k == pygame.K_k:
                    stav["rezim"] = "kresba"
                elif k == pygame.K_p:
                    stav["rezim"] = "plechovka"
                elif k == pygame.K_SPACE:
                    stav["rezim"] = "plechovka" if stav["rezim"] == "kresba" else "kresba"
                elif k == pygame.K_b:
                    i = ALGORITMY.index(stav["algoritmus"])
                    stav["algoritmus"] = ALGORITMY[(i + 1) % len(ALGORITMY)]
                elif k == pygame.K_n:
                    stav["susedstvo"] = 8 if stav["susedstvo"] == 4 else 4
                elif k == pygame.K_a:
                    stav["animacia"] = not stav["animacia"]
                elif k == pygame.K_UP:
                    stav["rychlost"] = min(stav["rychlost"] * 2, 200_000)
                elif k == pygame.K_DOWN:
                    stav["rychlost"] = max(stav["rychlost"] // 2, 10)
                elif k == pygame.K_c:
                    platno.fill(BIELA)
                    vyplnanie = None
                    stav["pocet"] = 0
                    stav["cas_ms"] = None
                elif pygame.K_1 <= k <= pygame.K_6:
                    stav["farba"] = PALETA[k - pygame.K_1]
                nastav_kurzor(stav["rezim"])

            elif udalost.type == pygame.MOUSEBUTTONDOWN and udalost.button == 1:
                if not je_na_platne(udalost.pos) or vyplnanie is not None:
                    continue
                bod = na_platno(udalost.pos)

                if stav["rezim"] == "kresba":
                    kreslim = True
                    posledny_bod = bod
                    pygame.draw.circle(platno, CIERNA, bod, HRUBKA // 2 + 1)
                elif stav["algoritmus"] == "DFS R":
                    # rekurzívne DFS sa nedá animovať -> vyplníme naraz a zmeriame čas
                    platno.lock()
                    zac = time.perf_counter()
                    stav["pocet"] = flood_fill_rekurzivne(platno, bod, stav["farba"])
                    stav["cas_ms"] = (time.perf_counter() - zac) * 1000
                    platno.unlock()
                else:
                    vyplnanie = flood_fill(platno, bod, stav["farba"],
                                           stav["algoritmus"], stav["susedstvo"])
                    stav["pocet"] = 0
                    stav["cas_ms"] = None
                    if not stav["animacia"]:
                        # bez animácie vyplníme všetko naraz a zmeriame čas
                        platno.lock()
                        zac = time.perf_counter()
                        for stav["pocet"] in vyplnanie:
                            pass
                        stav["cas_ms"] = (time.perf_counter() - zac) * 1000
                        platno.unlock()
                        vyplnanie = None

            elif udalost.type == pygame.MOUSEBUTTONUP and udalost.button == 1:
                kreslim = False
                posledny_bod = None

            elif udalost.type == pygame.MOUSEMOTION and kreslim:
                x, y = na_platno(udalost.pos)
                # bod "pritlačíme" na okraj plátna, aby čiara nevyšla von
                bod = (max(0, min(SIRKA - 1, x)), max(0, min(VYSKA - PANEL - 1, y)))
                # spájame úsečkou s predchádzajúcim bodom -> súvislá čiara
                pygame.draw.line(platno, CIERNA, posledny_bod, bod, HRUBKA)
                pygame.draw.circle(platno, CIERNA, bod, HRUBKA // 2 + 1)
                posledny_bod = bod

        # animované vypĺňanie: v každej snímke spracujeme kúsok
        if vyplnanie is not None:
            platno.lock()
            try:
                for _ in range(stav["rychlost"]):
                    stav["pocet"] = next(vyplnanie)
            except StopIteration:
                vyplnanie = None
            platno.unlock()

        okno.blit(platno, (0, PANEL))
        kresli_panel(okno, font, stav)
        pygame.display.flip()
        hodiny.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
