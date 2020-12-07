import os
import sys
import re
import random


def generator():
    plik1 = open("generator.txt", 'w')

    while True:
        ile = input('Type number of verticies: ')
        try:
            ile = int(ile)
            if ile > 1:
                break
            else:
                print('Number of verticies should be at least one!')
        except ValueError:
            print('Number of verticies should be an integer!')

    plik1.write(str(ile) + "\n")

    pary = []
    for i in range(1, ile + 1, 1):
        while True:
            a = random.randint(0, 200)
            b = random.randint(0, 200)
            if (a, b) not in pary:
                pary.append((a, b))
                break
        plik1.write(str(i) + " " + str(a) + " " + str(b) + "\n")

    plik1.close()
    return plik1.name


def choose_file():
    # pobieramy sciezke biezacego katalogu roboczego (cwd)
    file_dir = os.getcwd()
    # tworzymy liste zawartosci cwd
    dir_content = os.listdir(file_dir)
    # wybieramy z dir_content tylko pliki *.txt
    dir_txts = list(filter(lambda x: x[-4:] == '.txt', dir_content))
    dir_txts = ['generator'] + dir_txts

    print('\nYou can use data from: ')
    print(*dir_txts, sep='\n')

    while True:
        answer = input('Type which one would you like to use: ')

        if answer == 'generator':
            return generator()

        if answer in dir_txts:
            return answer

        else:
            print('Please, enter a correct name.')


# funkcja sprawdzajaca czy podany plik posiada poprawne dane
def check_file(filename):
    with open(filename, encoding='utf-8-sig') as file:
        lines = file.readlines()

        try:
            # sprawdzamy czy pierwsza linia to pojedyncza liczba typu int()
            number_of_lines = int(lines[0])
        except ValueError:
            print('First line should be a single integer value!')
            return False

        # sprawdzamy kazda linie po kolei (bez lini pierwszej)
        for index, line in enumerate(lines[1:]):

            # jesli lini jest wiecej niz wskazuje na to pierwsza linijka zwracamy False
            if index == number_of_lines:
                print('File has too many lines!')
                return False

            # wyrazenie regularne postaci: 'numer linii''spacja''liczba calkowita''spacja''liczba calkowita'
            # result = re.search('^' + str(index + 1) + ' -?\\d+ -?\\d+$', line)
            result = re.search(r'^\d+\s+(-?)\d+\s+(-?)\d+(\s+|$)', line)

            # jesli brak dopasowania dla linii i powyzszego regexpa zwracamy False
            if result is None:
                print(f'Invalid data in line {index + 2}')
                return False

        # jesli plik zawiera poprawne dane zwracamy True
        if index + 1 == number_of_lines:
            file.close()
            return True
        else:
            print('File has not enough lines!')
            return False


# funkcja liczaca odleglosc miedzy dwoma punktami
def distance(x1, y1, x2, y2):
    return round(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1 / 2), 3)


# funkcja tworzaca macierz, gdzie komorka [i][j] to odleglosc miedzy punktami i oraz j
def create_matrix(filename):
    with open(filename, encoding='utf-8-sig') as file:
        content = file.read()

    content = content.split('\n')
    number_of_verticies = int(content[0])

    # tworzeni tablicy krotek postaci (x,y) dla kazdego punktu
    a = []
    for number in range(1, number_of_verticies + 1):
        tmp = content[number].replace('  ', ' ').split(' ')
        a.append((int(tmp[1]), int(tmp[2])))

    # stworzenie macierzy
    matrix = []
    for vertex_index in range(number_of_verticies):
        distances = []
        for index in range(number_of_verticies):
            if index > vertex_index:
                distances.append(distance(a[vertex_index][0], a[vertex_index][1], a[index][0], a[index][1]))
            elif index < vertex_index:
                distances.append(matrix[index][vertex_index])
            else:
                distances.append(0)
        matrix.append(distances)

    # # wyswietl macierz
    # for row in matrix:
    #     for number in row:
    #         print("%4.3f" % number, end=' ')
    #     print('\n')

    return matrix


if __name__ == '__main__':
    f = choose_file()
    if check_file(f):
        create_matrix(f)
    else:
        sys.exit(0)
