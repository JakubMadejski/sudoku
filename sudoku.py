import pygame
import sys
import random
import copy

pygame.init()
SZEROKOSC, WYSOKOSC = 600, 710
OKNO = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption("Sudoku - Gra")

BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)
NIEBIESKI = (50, 50, 255)
SZARY = (100, 100, 100)
JASNY_SZARY = (200, 200, 200)
CZERWONY = (255, 0, 0)
ZOLTY = (255, 255, 153)
ZIELONY = (0, 200, 0)

CZCIONKA = pygame.font.SysFont("Arial", 40)
CZCIONKA_MALA = pygame.font.SysFont("Arial", 30)
CZCIONKA_DUZA = pygame.font.SysFont("Arial", 80)

PLANSZE = [
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0], [6, 0, 0, 1, 9, 5, 0, 0, 0], [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3], [4, 0, 0, 8, 0, 3, 0, 0, 1], [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0], [0, 0, 0, 4, 1, 9, 0, 0, 5], [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],
    [
        [0, 0, 0, 2, 6, 0, 7, 0, 1], [6, 8, 0, 0, 7, 0, 0, 9, 0], [1, 9, 0, 0, 0, 4, 5, 0, 0],
        [8, 2, 0, 1, 0, 0, 0, 4, 0], [0, 0, 4, 6, 0, 2, 9, 0, 0], [0, 5, 0, 0, 0, 3, 0, 2, 8],
        [0, 0, 9, 3, 0, 0, 0, 7, 4], [0, 4, 0, 0, 5, 0, 0, 3, 6], [7, 0, 3, 0, 1, 8, 0, 0, 0]
    ],
    [
        [1, 0, 0, 4, 8, 9, 0, 0, 6], [7, 3, 0, 0, 0, 0, 0, 4, 0], [0, 0, 0, 0, 0, 1, 2, 9, 5],
        [0, 0, 7, 1, 2, 0, 6, 0, 0], [5, 0, 0, 7, 0, 3, 0, 0, 8], [0, 0, 6, 0, 9, 5, 7, 0, 0],
        [9, 1, 4, 6, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 3, 7], [8, 0, 0, 5, 1, 2, 0, 0, 4]
    ]
]

plansza = copy.deepcopy(random.choice(PLANSZE))
rozwiazana_plansza = copy.deepcopy(plansza)

def czy_pasuje(p, wiersz, kolumna, liczba):
    for i in range(9):
        if p[wiersz][i] == liczba and kolumna != i: return False
    for i in range(9):
        if p[i][kolumna] == liczba and wiersz != i: return False
    kw_x, kw_y = (kolumna // 3) * 3, (wiersz // 3) * 3
    for i in range(kw_y, kw_y + 3):
        for j in range(kw_x, kw_x + 3):
            if p[i][j] == liczba and (i, j) != (wiersz, kolumna): return False
    return True

def znajdz_puste(p):
    for w in range(9):
        for k in range(9):
            if p[w][k] == 0: return (w, k)
    return None

def rozwiaz(p):
    puste = znajdz_puste(p)
    if not puste: return True
    w, k = puste

    for liczba in range(1, 10):
        if czy_pasuje(p, w, k, liczba):
            p[w][k] = liczba
            if rozwiaz(p): return True
            p[w][k] = 0
    return False

rozwiaz(rozwiazana_plansza)

zablokowane = set()
for w in range(9):
    for k in range(9):
        if plansza[w][k] != 0:
            zablokowane.add((w, k))

zaznaczone = None
podswietlona_liczba = None
bledy = 0
bledne_wpisy = {}

def czy_wygrana():
    for w in range(9):
        for k in range(9):
            if plansza[w][k] == 0: return False
    return True

def zlicz_cyfry(p, cyfra):
    licznik = 0
    for w in range(9):
        for k in range(9):
            if p[w][k] == cyfra:
                licznik += 1
    return licznik

def rysuj_podswietlenie():
    if podswietlona_liczba is not None:
        for w in range(9):
            for k in range(9):
                if plansza[w][k] == podswietlona_liczba:
                    pygame.draw.rect(OKNO, ZOLTY, (k * 66, w * 66, 66, 66))

def rysuj_siatke():
    for i in range(10):
        grubosc = 4 if i % 3 == 0 else 1
        pygame.draw.line(OKNO, CZARNY, (0, i * 66), (SZEROKOSC, i * 66), grubosc)
        pygame.draw.line(OKNO, CZARNY, (i * 66, 0), (i * 66, 600), grubosc)

    if zaznaczone:
        wiersz, kolumna = zaznaczone
        pygame.draw.rect(OKNO, CZERWONY, (kolumna * 66, wiersz * 66, 66, 66), 3)

def rysuj_liczby():
    for w in range(9):
        for k in range(9):
            if plansza[w][k] != 0:
                kolor = SZARY if (w, k) in zablokowane else NIEBIESKI
                tekst = CZCIONKA.render(str(plansza[w][k]), True, kolor)
                OKNO.blit(tekst, (k * 66 + 20, w * 66 + 10))
    for (w, k), liczba in bledne_wpisy.items():
        tekst = CZCIONKA.render(str(liczba), True, CZERWONY)
        OKNO.blit(tekst, (k * 66 + 20, w * 66 + 10))

def formatuj_czas(czas_ms):
    sekundy = (czas_ms // 1000) % 60
    minuty = czas_ms // 60000
    return f"{minuty:02}:{sekundy:02}"

def main():
    global zaznaczone, bledy, podswietlona_liczba
    wygrana = False
    start_czas = pygame.time.get_ticks()
    czas_koncowy = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if not wygrana:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    poz = pygame.mouse.get_pos()
                    k, w = poz[0] // 66, poz[1] // 66
                    if k < 9 and w < 9:
                        zaznaczone = (w, k)
                        if plansza[w][k] != 0:
                            podswietlona_liczba = plansza[w][k]
                        else:
                            podswietlona_liczba = None

                if event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        if zaznaczone is None:
                            zaznaczone = (0, 0)
                        else:
                            w, k = zaznaczone
                            if event.key == pygame.K_UP: w = max(0, w - 1)
                            elif event.key == pygame.K_DOWN: w = min(8, w + 1)
                            elif event.key == pygame.K_LEFT: k = max(0, k - 1)
                            elif event.key == pygame.K_RIGHT: k = min(8, k + 1)
                            zaznaczone = (w, k)
                        
                        w, k = zaznaczone
                        podswietlona_liczba = plansza[w][k] if plansza[w][k] != 0 else None

                    elif zaznaczone:
                        w, k = zaznaczone
                        if (w, k) not in zablokowane:
                            if event.unicode.isdigit() and event.unicode != '0':
                                liczba = int(event.unicode)
                                if liczba == rozwiazana_plansza[w][k]:
                                    plansza[w][k] = liczba
                                    bledne_wpisy.pop((w, k), None)
                                    podswietlona_liczba = liczba
                                else:
                                    plansza[w][k] = 0
                                    bledne_wpisy[(w, k)] = liczba
                                    bledy += 1
                            elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                                plansza[w][k] = 0
                                bledne_wpisy.pop((w, k), None)

        OKNO.fill(BIALY)
        rysuj_podswietlenie()
        rysuj_siatke()
        rysuj_liczby()
        
        for i in range(1, 10):
            ilosc = zlicz_cyfry(plansza, i)
            kolor_tekstu = JASNY_SZARY if ilosc == 9 else CZARNY
            tekst_cyfry = CZCIONKA_MALA.render(str(i), True, kolor_tekstu)
            x_pos = 15 + i * 55
            OKNO.blit(tekst_cyfry, (x_pos, 615))
            if ilosc == 9:
                pygame.draw.line(OKNO, CZERWONY, (x_pos - 5, 635), (x_pos + 20, 635), 3)

        tekst_bledow = CZCIONKA_MALA.render(f"Błędy: {bledy}", True, CZERWONY)
        OKNO.blit(tekst_bledow, (20, 665))

        if not wygrana:
            aktualny_czas = pygame.time.get_ticks() - start_czas
        else:
            aktualny_czas = czas_koncowy

        tekst_czasu = CZCIONKA_MALA.render(f"Czas: {formatuj_czas(aktualny_czas)}", True, CZARNY)
        OKNO.blit(tekst_czasu, (440, 665))

        if czy_wygrana() and not wygrana:
            wygrana = True
            czas_koncowy = aktualny_czas
        
        if wygrana:
            tekst_wygrana = CZCIONKA_DUZA.render("WYGRANA!", True, ZIELONY)
            pygame.draw.rect(OKNO, BIALY, (80, 250, 440, 100)) 
            OKNO.blit(tekst_wygrana, (110, 260))

        pygame.display.update()

if __name__ == "__main__":
    main()