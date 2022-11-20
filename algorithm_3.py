import sys
import random

class Item:
    def __init__(self, w, v, c, o):
        self.w = w
        self.v = v
        self.c = c
        self.o = o


class Node:
    def __init__(self, s, f):
        self.s = s
        self.f = f


def init(input_path):
    global W, m, n, items, ans
    items = []
    ans = [0, 0]
    with open(input_path) as file:
        W = int(file.readline().rstrip())
        m = int(file.readline().rstrip())
        w = list(map(int, file.readline().rstrip().split(",")))
        v = list(map(int, file.readline().rstrip().split(",")))
        c = list(map(int, file.readline().rstrip().split(",")))
        n = len(w)
        if (n != len(v) or n != len(v)):
            print('input error: w[] and v[] and c[] must have the same length')
            sys.exit(0)
        for i in range(n):
            items.append(Item(w[i], v[i], c[i], i))
        # sort items heuristically by ratio of value/weight
        items = sorted(items, key=lambda item: item.v/item.w, reverse=True)


def commit(output_path):
    global ans, items
    traslatedAnsState = 0

    for i in range(n):
        if (ans[1] & (1 << i)):
            traslatedAnsState |= (1 << items[i].o)

    with open(output_path, "w") as file:
        print(ans[0], file=file) 
        output_str = ""
        for i in range(n):
            if (traslatedAnsState & (1 << i)):
                output_str += "1"
            else:
                output_str += "0"
            if (i != n):
                output_str += ", "
        print(output_str, file=file)


def fitness(state):
    global W, m, ans
    v = 0
    w = 0
    setOfClass = set()
    for i in range(n):
        if (state & (1 << i)):
            v += items[i].v
            w += items[i].w
            setOfClass.add(items[i].c)
        
    if (w > W):
        return 0

    if (len(setOfClass) == m and v > ans[0]):
        ans = [v, state]
    
    for i, item in enumerate(items):
        if ((state & (1 << n)) == 0):
            if (w + item.w < W):
                v += item.v
                w += item.w
            else:
                v += item.v * ((W - w)/item.w)
    
    if (len(setOfClass) != m):
        v *= round(len(setOfClass)/m)

    return v


def getNeighbors(state):
    neighbors = []
    for i in range(n): 
        new_state = state ^ (1 << i)
        neighbors.append(Node(new_state, fitness(new_state)))
    return neighbors


def initializePopulation():
    parents = [random.randint(0, (1<<n)-1) for _ in range(population_size)]
    fitness_scores = [fitness(parent) for parent in parents]
    total = sum(fitness_scores)
    while (total == 0):
        parents = [random.randint(0, (1<<n)-1) for _ in range(population_size)]
        fitness_scores = [fitness(parent) for parent in parents]
        total = sum(fitness_scores)
    return parents


def process():
    global population, population_size, max_stack_size

    # initialize population
    population = initializePopulation()
    
    # local beam search
    for _ in range(max_stack_size):
        neighbors = []
        for node in population:
            neighbors.extend(getNeighbors(node))

        # get best <population_size> neighbors
        neighbors = sorted(neighbors, key=lambda neighbor: neighbor.f, reverse=True)[:population_size]
        
        if (neighbors[0].f == 0):
            population = initializePopulation()
            continue

        population = [neighbor.s for neighbor in neighbors]


def main(input_path, output_path):
    init(input_path)
    process()
    commit(output_path)


if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print('usage:\talgorithm_3.py <input_file> <output_file> <population_size(optional)> <max_stack_size(optional)>')
        sys.exit(0)
    global population_size, max_stack_size
    population_size = 10 if (len(sys.argv) <= 3) else int(sys.argv[3]) 
    max_stack_size = 500 if (len(sys.argv) <= 4) else int(sys.argv[4])
    main(sys.argv[1],sys.argv[2])
