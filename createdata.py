import os, sys, re, random

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
            a = random.randint(1, 200)
            b = random.randint(1, 200)
            if (a, b) not in pary:
                pary.append((a, b))
                break
        plik1.write(str(i) + " " + str(a) + " " + str(b) + "\n")
    plik1.close()
    return plik1.name

# #funkcja zwracajaca nazwe pliku z danymi wejsciowymi
# def choose_file():
#     fileDir = os.getcwd()   #pobieramy sciezke biezacego katalogu roboczego (cwd)
#     dirContent = os.listdir(fileDir)    #tworzymy liste zawartosci cwd
#     dirTxts = list(filter(lambda x: x[-4:] == '.txt', dirContent))  #wybieramy z dirContent tylko pliki *.txt

#     #jeśli w ced nie ma plików txt generujemy sobie taki
#     if len(dirTxts) == 0:
#         print('No txt file in this directory!\nData will be generated.')
#         f = generator()
#         return f

#     #jesli jest tylko jeden plik txt bedziemy dalej na nim pracowac
#     elif len(dirTxts) == 1:
#         print(f'Data will be read from {dirTxts[0]}')
#         return dirTxts[0]

#     #jesli jest wiecej niz 1 plik txt pozwalamy uzytkownikowi wybrac
#     else:
#         print(f'In {fileDir} are {len(dirTxts)} txt files:')
#         print(*(dirTxts), sep='\n')
#         while True:
#             answer = input('Type which one would you like to use: ')
#             if answer in dirTxts:
#                 return answer
#             else:
#                 print('Please, enter a valid file name.')

def choose_file():

    fileDir = os.getcwd()   #pobieramy sciezke biezacego katalogu roboczego (cwd)
    dirContent = os.listdir(fileDir)    #tworzymy liste zawartosci cwd
    dirTxts = list(filter(lambda x: x[-4:] == '.txt', dirContent))  #wybieramy z dirContent tylko pliki *.txt
    dirTxts = ['generator'] + dirTxts

    print('\nYou can use data from: ')
    print(*(dirTxts), sep='\n')

    while True:
        answer = input('Type which one would you like to use: ')
        
        if answer == 'generator':
            return generator()

        if answer in dirTxts:
            return answer

        else:
            print('Please, enter a correct name.')


#funkcja sprawdzajaca czy podany plik posiada poprawne dane
def check_file(filename):

    file = open(filename, 'r')
    lines = file.readlines()

    try:
        number_of_lines = int(lines[0])     #sprawdzamy czy pierwsza linia to pojedyncza liczba typu int()
    except ValueError:
        print('First line should be a single integer value!')   #jesli nie zwracamy False
        return False

    for index, line in enumerate(lines[1:]):    #sprawdzamy kazda linie po kolei (bez lini pierwszej)

        if index == number_of_lines:    #jesli lini jest wiecej niz wskazuje na to pierwsza linijka zwracamy False
            print('File has too many lines!')
            return False

        result = re.search('^' + str(index+1) + ' \d+ \d+$', line) #wyrazenie regularne postaci: 'numer linii''spacja''liczba calkowita''spacja''liczba calkowita'

        if result == None:      #jesli brak dopasowania dla linii i powyzszego regexpa zwracamy False
            print(f'Invalid data in line {index + 2}')
            return False
    
    if index + 1 == number_of_lines:
        file.close()    #jesli plik zawiera poprawne dane zwracamy True
        return True
    else:
        print('File has not enough lines!')
        return False

#funkcja liczaca odleglosc miedzy dwoma punktami
def distance(x1, y1, x2, y2):
    return round(( (x2 - x1)**2 + (y2 - y1)**2 )**(1/2), 3)

#funkcja tworzaca macierz, gdzie komorka [i][j] to odleglosc miedzy punktami i oraz j
def create_matrix(filename):

    file = open(filename, 'r')

    content = file.read()
    content = content.split('\n')
    print(content[1:])
    number_of_verticies = int(content[0])
    #tworzeni tablicy krotek postaci (x,y) dla kazdego punktu
    a = []
    for number in range(1, number_of_verticies + 1):
        tmp = content[number].split(' ')
        a.append( (int(tmp[1]), int(tmp[2])) )

    #stworzenie macierzy
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

    #wyswietl macierz
    for row in matrix:
        for number in row:
            print("%4.3f"%number, end='\t')
        print('\n')

    return matrix


if __name__ == '__main__':
    f = choose_file()
    if check_file(f):
        create_matrix(f)
    else:
        sys.exit(0)
