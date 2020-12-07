import createdata
import random


def calculate_fitness(matrix, route):

    distance = 0
    for index in range(len(route) - 1):
        distance += matrix[route[index]][route[index + 1]]

    return round(distance, 3)


def calculate_fitness_of_generation(matrix, generation):

    result = []
    for route in generation:
        distance = 0
        route += [route[0]]
        for index in range(len(route) - 1):
            distance += matrix[route[index]][route[index + 1]]
        result.append((route, round(distance, 3)))

    return result


def calculate_fitness_of_generation2(generation, matrix):

    result = []
    for route in generation:
        distance = 0
        tmp_route = route + [route[0]]
        for index in range(len(tmp_route) - 1):
            distance += matrix[tmp_route[index]][tmp_route[index + 1]]
        result.append(round(distance, 3))

    return result


def find_shortest_route(generation, matrix):

    routes = calculate_fitness_of_generation2(generation, matrix)

    return min(routes)


def tournament(generation, matrix):

    distances = calculate_fitness_of_generation2(generation, matrix)
    generation_with_distance = list(zip(generation, distances))

    new_generation = []
    while len(new_generation) != parents_for_next_generation:
        random.shuffle(generation_with_distance)
        for route in sorted(generation_with_distance[:parents_for_next_generation], key=lambda pair: pair[1]):
            if route[0] not in new_generation:
                new_generation.append(route[0])
                break

    return new_generation


def choose_the_best(generation, matrix):

    distances = calculate_fitness_of_generation2(generation, matrix)
    generation_with_distance = zip(distances, generation)

    result = [x for _, x in sorted(generation_with_distance)]

    return result[:parents_for_next_generation]


# def tournament(generation, matrix):
#
#     generation_with_distance = calculate_fitness_of_generation(matrix, generation)
#     result = []
#     for _ in range(parents_for_next_generation):
#         random.shuffle(generation_with_distance)
#         for route in sorted(generation_with_distance[:parents_for_next_generation], key=lambda pair: pair[1]):
#             if route not in result:
#                 result.append(route[0])
#                 # print(route)
#                 break
#     index = 0
#     while len(result) != parents_for_next_generation:
#         if generation_with_distance[index] not in result:
#             result.append(generation_with_distance[index])
#         index += 1
#
#     return result


def rank_based_wheel_selection(generation):

    shots = []
    for _ in range(parents_for_next_generation):
        shots.append(random.randint(1, (1 + size_of_generation)//2 * size_of_generation + 1))
    shots = sorted(shots)
    n = 1
    result = []
    for index, route in enumerate(sorted(generation, key=lambda pair: pair[1])):
        if len(result) == parents_for_next_generation:
            break
        else:
            for shot in shots:
                if n <= shot <= n + size_of_generation - index - 1:
                    result.append(route)
        n += size_of_generation - index
    return result


def pmx(parent1, parent2):

    length = len(parent1)
    # point1 = random.randint(0, length//2)
    # point2 = random.randint(length//2 + 1, length - 1)

    point1 = random.randint(0, length - 2)
    point2 = random.randint(point1, length - 1)

    child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
    child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]

    for x in range(length):

        if x in range(point1, point2):
            continue

        while child1[x] in child1[point1:point2]:

            child1[x] = child2[child1.index(child1[x], point1, point2)]

        while child2[x] in child2[point1:point2]:

            child2[x] = child1[child2.index(child2[x], point1, point2)]

    # print(parent1, parent2)
    # print(point1, point2)
    # print(child1, child2)

    return child1, child2


def mutate(generation):

    for route in generation:

        chance = random.randint(1, 100)
        if chance <= 10:

            a = random.randint(0, len(route) - 2)
            b = random.randint(a, len(route) - 1)
            route[a], route[b] = route[b], route[a]

    return generation


size_of_generation = 200
parents_for_next_generation = int(size_of_generation * 0.5)


def main():

    while True:
        file = createdata.choose_file()
        if createdata.check_file(file):
            matrix = createdata.create_matrix(file)
            break
        else:
            print("Choose another file or use a generator.")

    cities = [x for x in range(len(matrix))]
    generation = []

    while len(generation) < size_of_generation:
        route = random.sample(cities, len(cities))
        if route not in generation:
            generation.append(route)

    for row in matrix:
        print(row)

    for i in range(1000):

        print(i + 1, ": ", find_shortest_route(generation, matrix))

        random.shuffle(generation)

        generation = tournament(generation, matrix)
        # generation = choose_the_best(generation, matrix)

        available_parents = [x for x in range(0, len(generation))]

        while available_parents:

            parent1_index = random.choice(available_parents)
            available_parents.remove(parent1_index)

            parent2_index = random.choice(available_parents)
            available_parents.remove(parent2_index)

            tmp1, tmp2 = pmx(generation[parent1_index], generation[parent2_index])
            generation.append(tmp1)
            generation.append(tmp2)

        generation = mutate(generation)


if __name__ == '__main__':
    main()
