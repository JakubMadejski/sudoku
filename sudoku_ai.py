import gymnasium as gym
from gymnasium import spaces
import numpy as np
import copy
import random

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

class SudokuEnv(gym.Env):
    def __init__(self):
        super(SudokuEnv, self).__init__()
        # Akcja to 3 liczby: [wiersz (0-8), kolumna (0-8), cyfra (0-8, czyli 1-9)]
        self.action_space = spaces.MultiDiscrete([9, 9, 9])
        # Stan gry to plansza 9x9
        self.observation_space = spaces.Box(low=0, high=9, shape=(9, 9), dtype=np.int8)
        self.max_kroki = 200 # Zabezpieczenie przed graniem w nieskończoność

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.oryginalna = copy.deepcopy(random.choice(PLANSZE))
        self.plansza = copy.deepcopy(self.oryginalna)
        
        # Tworzymy rozwiązaną planszę, żeby AI wiedziało, czy dobrze zgadło
        self.rozwiazana = copy.deepcopy(self.oryginalna)
        self._rozwiaz(self.rozwiazana)
        
        self.kroki = 0
        return np.array(self.plansza, dtype=np.int8), {}

    def step(self, action):
        w, k, wartosc = action[0], action[1], action[2] + 1
        nagroda = 0
        zakonczone = False
        self.kroki += 1

        if self.oryginalna[w][k] != 0:
            nagroda = -1  # Kara za zmianę liczby z oryginalnej planszy
        elif wartosc == self.rozwiazana[w][k]:
            if self.plansza[w][k] == 0:
                nagroda = 1  # Nagroda za poprawną nową cyfrę
                self.plansza[w][k] = wartosc
            else:
                nagroda = -0.1 # Kara za klikanie w to samo odgadnięte miejsce
        else:
            nagroda = -1  # Kara za błędną cyfrę
            
        if np.array_equal(self.plansza, self.rozwiazana):
            nagroda = 10  # Ekstra nagroda za wygraną
            zakonczone = True

        uciete = self.kroki >= self.max_kroki
        return np.array(self.plansza, dtype=np.int8), nagroda, zakonczone, uciete, {}

    # --- Logika z Twojego kodu Pygame ---
    def _czy_pasuje(self, p, wiersz, kolumna, liczba):
        for i in range(9):
            if p[wiersz][i] == liczba and kolumna != i: return False
            if p[i][kolumna] == liczba and wiersz != i: return False
        kw_x, kw_y = (kolumna // 3) * 3, (wiersz // 3) * 3
        for i in range(kw_y, kw_y + 3):
            for j in range(kw_x, kw_x + 3):
                if p[i][j] == liczba and (i, j) != (wiersz, kolumna): return False
        return True

    def _znajdz_puste(self, p):
        for w in range(9):
            for k in range(9):
                if p[w][k] == 0: return (w, k)
        return None

    def _rozwiaz(self, p):
        puste = self._znajdz_puste(p)
        if not puste: return True
        w, k = puste
        for liczba in range(1, 10):
            if self._czy_pasuje(p, w, k, liczba):
                p[w][k] = liczba
                if self._rozwiaz(p): return True
                p[w][k] = 0
        return False