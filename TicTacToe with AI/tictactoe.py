# importy
import random
from random import randint
import time

# defenicje funkcji, klas i inne
def jeden_D_to_2D(jeden_D):
    dwa_D = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
    for i in range(3):
        dwa_D[2][i] = jeden_D[i]
    for i in range(3):
        dwa_D[1][i] = jeden_D[i+3]
    for i in range(3):
        dwa_D[0][i] = jeden_D[i+6]
    return dwa_D

def print_pole(pole2D):
    print("---------")
    print(f"| {pole2D[2][0]} {pole2D[2][1]} {pole2D[2][2]} |")
    print(f"| {pole2D[1][0]} {pole2D[1][1]} {pole2D[1][2]} |")
    print(f"| {pole2D[0][0]} {pole2D[0][1]} {pole2D[0][2]} |")
    print("---------")

def put_coordinates(pole, symbol):
    print("Enter the coordinates:")
    while True:
        try:
            y, x = input().split()
            x, y = int(x), int(y)
        except ValueError:
            print("You should enter numbers!")
            continue
        if x < 1 or y < 1 or x > 3 or y > 3:
            print("Coordinates should be from 1 to 3!")
            continue
        elif pole[x - 1][y - 1] in ['X', 'O']:
            print("This cell is occupied! Choose another one!")
            continue
        break   # wychodzi z pętli, jeśli żaden z warunków nie został spełniony
    pole[x - 1][y - 1] = symbol
    return pole

def put_coordinates_easy_AI(pole, symbol):
    random.seed()
    while True:
        x, y = randint(1, 3), randint(1, 3)
        if pole[x - 1][y - 1] in ['X', 'O']:
            continue
        break   # wychodzi z pętli, jeśli żaden z warunków nie został spełniony
    pole[x - 1][y - 1] = symbol
    return pole

def put_coordinates_medium_AI(pole, symbol):
    def check_two_in_line(pole, symb, symbol):  # symb - symbol sprawdzany, symbol - symbol stawiany
        licznik_punktow_wierszu = 0
        for i in range(3):
            for j, klatka in enumerate(pole[i]):     # sprawdza wiersze
                if klatka == symb: licznik_punktow_wierszu += 1
                if klatka == '_':
                    licznik_punktow_wierszu += 5
                    a, b = i, j
            if licznik_punktow_wierszu == 7:   # dwa symbole (1) i jeden '_' (5)
                pole[a][b] = symbol
                return pole
            licznik_punktow_wierszu = 0

            for j, klatka in enumerate([pole[0][i], pole[1][i], pole[2][i]]):     # sprawdza wiersze
                if klatka == symb: licznik_punktow_wierszu += 1
                if klatka == '_':
                    licznik_punktow_wierszu += 5
                    a, b = j, i
            if licznik_punktow_wierszu == 7:   # dwa symbole (1) i jeden '_' (5)
                pole[a][b] = symbol
                return pole
            licznik_punktow_wierszu = 0
        for i in range(3):
            if pole[i][i] == symb: licznik_punktow_wierszu +=1
            if pole[i][i] == '_':
                licznik_punktow_wierszu +=5
                a, b = i, i
        if licznik_punktow_wierszu == 7:
            pole[a][b] = symbol
            return pole
        licznik_punktow_wierszu = 0
        for i in range(3):
            if pole[2 - i][i] == symb: licznik_punktow_wierszu +=1
            if pole[2 - i][i] == '_':
                licznik_punktow_wierszu +=5
                a, b = 2 - i, i
        if licznik_punktow_wierszu == 7:
            pole[a][b] = symbol
            return pole
        licznik_punktow_wierszu = 0


    if symbol == 'X':
        antisymbol = 'O'
    elif symbol == 'O':
        antisymbol = 'X'
    if check_two_in_line(pole, symbol, symbol) != None:     # napierw sprawdza się, czy da się wygrać grę w jednej turze
        return pole
    elif check_two_in_line(pole, antisymbol, symbol) != None:     # potem, czy da się zablokować wygraną przeciwnikowi
        return pole

    put_coordinates_easy_AI(pole, symbol)

def make_turn(pole, symbol, player):
    if player == 'user':
        pole = put_coordinates(pole, symbol)
    elif player == 'easy':
        print("Making move level \"easy\"")
        put_coordinates_easy_AI(pole, symbol)
        # time.sleep(1)
    elif player == 'medium':
        print("Making move level \"medium\"")
        put_coordinates_medium_AI(pole, symbol)
        # time.sleep(1)
    print_pole(pole)

def check_win_state(pole, symbol):
    for i in range(3):
        if all(klatka == symbol for klatka in pole[i]):     # sprawdza wiersze
            return f"{symbol} wins"
        if all(klatka == symbol for klatka in [pole[0][i], pole[1][i], pole[2][i]]):    # sprawdza kołumny
            return f"{symbol} wins"
    if all(klatka == symbol for klatka in [pole[0][0], pole[1][1], pole[2][2]]):    # sprawdza jedną przekątną
            return f"{symbol} wins"
    if all(klatka == symbol for klatka in [pole[2][0], pole[1][1], pole[0][2]]):    # sprawdza drugą przekątną
            return f"{symbol} wins"

def check_game_state(pole):
    if check_win_state(pole, 'X') != None:
        print(check_win_state(pole, 'X'))
    elif check_win_state(pole, 'O') != None:
        print(check_win_state(pole, 'O'))
    elif any(klatka == '_' for klatka in pole[0]):
        return "Game not finished"
    elif any(klatka == '_' for klatka in pole[1]):
        return "Game not finished"
    elif any(klatka == '_' for klatka in pole[2]):
        return "Game not finished"
    else:
        print("Draw")



# program główny
while True:     # menu loop
    print("input command:")
    try:
        start, player1, player2 = input().split()
    except ValueError:
        continue
    break

pole = '_________'
pole = jeden_D_to_2D(pole)
print_pole(pole)
while True:
    make_turn(pole=pole, player=player1, symbol='X')
    if check_game_state(pole) != "Game not finished":
        break

    make_turn(pole=pole, player=player2, symbol='O')
    if check_game_state(pole) != "Game not finished":
        break

