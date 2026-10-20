"""
Jazdec na šachovnici – prehľadávanie do šírky (BFS)

Každý agent je jedna cesta (n-tica políčok). V každom kole sa každý agent
rozdelí na nových agentov – jeden pre každý možný ťah na ešte nenavštívené políčko.
Počet skúmaných ciest = stepcnt = počet vyskúšaných ťahov (rovnako ako v JazdecDFS.py).
Zložitosť O(8^(n*n)), navyše si BFS musí pamätať celú jednu úroveň stromu naraz.
"""
import json
import sys
import time

from JazdecDFS import STARTY, TAHY


def jazdec_bfs(n, x, y, limit_s=None, max_agentov=None):
    """
    Vráti (našiel_cestu, cesta, počet skúmaných ciest, čas v ms, dokončené).
    Beh sa preruší (dokončené = False), ak prekročí limit_s sekúnd
    alebo ak si naraz pamätá viac ako max_agentov ciest.
    """
    stepcnt = 0
    dalsia_kontrola = 1_000_000
    zac = time.perf_counter()
    koniec = zac + limit_s if limit_s else None

    def vysledok(nasiel, cesta, dokoncene):
        return nasiel, cesta, stepcnt, (time.perf_counter() - zac) * 1000, dokoncene

    agentiBFS = [((x, y),)]
    while agentiBFS:
        noviAgenti = []
        for agent in agentiBFS:
            if len(agent) == n * n:
                return vysledok(True, agent, True)
            ax, ay = agent[-1]
            for dx, dy in TAHY:
                stepcnt += 1
                nx, ny = ax + dx, ay + dy
                if 0 <= nx < n and 0 <= ny < n:
                    if (nx, ny) in agent: continue
                    noviAgenti.append(agent + ((nx, ny),))

            if stepcnt >= dalsia_kontrola:
                dalsia_kontrola += 1_000_000
                if koniec is not None and time.perf_counter() > koniec:
                    return vysledok(None, None, False)
                if max_agentov is not None and len(noviAgenti) > max_agentov:
                    return vysledok(None, None, False)

        agentiBFS = noviAgenti      # ďalšia úroveň stromu
    return vysledok(False, None, True)


if __name__ == "__main__":
    # python JazdecBFS.py [limit v sekundách] [max. počet ciest v pamäti]
    limit_s = float(sys.argv[1]) if len(sys.argv) > 1 else 600
    max_agentov = int(sys.argv[2]) if len(sys.argv) > 2 else 20_000_000
    vysledky = []

    for velkost, x, y in STARTY:
        nasiel, cesta, kroky, cas_ms, dokoncene = jazdec_bfs(velkost, x, y, limit_s, max_agentov)
        stav = nasiel if dokoncene else "prerušené (limit času / pamäte)"
        print(f"n = {velkost}  x,y = ({x},{y})  {stav}  {kroky:15_} ciest  {cas_ms:14.3f} ms".replace("_", " "))
        vysledky.append({"n": velkost, "x": x, "y": y, "nasiel": nasiel, "kroky": kroky,
                         "cas_ms": cas_ms, "dokoncene": dokoncene,
                         "limit_s": limit_s, "max_agentov": max_agentov})

    with open("vysledky_jazdec_bfs.json", "w", encoding="utf-8") as f:
        json.dump(vysledky, f, ensure_ascii=False, indent=2)
