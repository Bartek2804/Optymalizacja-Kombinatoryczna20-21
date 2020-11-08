import random, sys
import createdata as cd


def calculate(matrix):
    visited = [0]   #wierzchołki w kolejności w jakiej nalezy je odwiedzić
    road = 0    #całkowita odległość do pokonania

    #dla każdego wierzchołka znajdz najblizeszego sasiada
    while(len(visited) < len(matrix)):
        i = visited[-1]
        mintmp = 0
        minindex = 0
        for index, value in enumerate(matrix[i]):
            #nie można pojechać do samego siebie oraz już do odwiedzonego wierzchołka
            if value != 0 and index not in visited:
                #jak mintmp podstaw pierwsze miasto spełniające powyższy warunek
                if mintmp == 0:
                    mintmp = value
                    minindex = index
                elif mintmp > value:
                    mintmp = value
                    minindex = index
        visited.append(minindex)
        road += mintmp

    print('The distance is equal to: ', road + matrix[minindex][0])
    print(*(visited + [0]), sep=' -> ')

def main():
    while True:
        file = cd.choose_file()
        if cd.check_file(file):
            matrix = cd.create_matrix(file)
            calculate(matrix)
            break
        else:
            print("Choose another file or use a generator.")
        

if __name__ == '__main__':
    main()



