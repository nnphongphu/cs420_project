import sys
import random
import numpy.random as npr

class Item:
  def __init__(self, w, v, c, o):
    self.w = w
    self.v = v
    self.c = c
    self.o = o


class Node:
    def __init__(self, s, v, w, f):
        self.s = s
        self.v = v
        self.w = w
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


def fitness(chromosome):
    global W, m, ans
    v = 0
    w = 0
    setOfClass = set()
    for i in range(n):
        if (chromosome & (1 << i)):
            v += items[i].v
            w += items[i].w
            setOfClass.add(items[i].c)
        
    if (w > W):
        return 0

    if (len(setOfClass) == m and v > ans[0]):
        ans = [v, chromosome]
    
    for i, item in enumerate(items):
        if ((chromosome & (1 << n)) == 0):
            if (w + item.w < W):
                v += item.v
                w += item.w
            else:
                v += item.v * ((W - w)/item.w)
    
    if (len(setOfClass) != m):
        v *= round(len(setOfClass)/m)

    return v


def rouletteSelectOne(selection_probs):
    global population_size, parents
    return parents[npr.choice(range(population_size), p=selection_probs)]


def crossover(chroA, chroB):
    global n
    slit = random.randint(0, n)
    chroA1 = chroA & (~0 << slit)
    chroA2 = chroA & ((1 << slit) - 1)
    chroB1 = chroB & (~0 << slit)
    chroB2 = chroB & ((1 << slit) - 1)
    return chroA1 | chroB2, chroA2 | chroB1


def mutate(chromosome):
    global n
    for i in range(n):		
        prob = random.uniform(0, 1)
        if prob > 0.5:
            chromosome ^= (1 << i)
    return chromosome


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
    global parents, population_size, max_stack_size, items

    # population initialization
    parents = initializePopulation()

    for _ in range(max_stack_size):
        # fitness assignment
        fitness_scores = [fitness(parent) for parent in parents]

        #selection
        total = sum(fitness_scores)
        if (total == 0):
            parents = initializePopulation()
            continue

        selection_probs = [fitness_score/total for fitness_score in fitness_scores]
        selected_parents = [rouletteSelectOne(selection_probs) for _ in range(population_size)]

        #crossover
        new_parents = []
        for i in range(0, population_size, 2):
            nchild1, nchild2 = crossover(selected_parents[i], selected_parents[(i+1) % population_size])
            new_parents.append(nchild1)
            new_parents.append(nchild2)
        
        #mutation
        new_parents = [mutate(new_parent) for new_parent in new_parents]
        parents = new_parents

    # finalize
    fitness_scores = [fitness(parent) for parent in parents]


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


def main(input_path, output_path):
    init(input_path)
    process()
    commit(output_path)


if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print('usage:\talgorithm_4.py <input_file> <output_file> <population_size(optional)> <max_stack_size(optional)>')
        sys.exit(0)
    global population_size, max_stack_size
    population_size = 120 if (len(sys.argv) <= 3) else int(sys.argv[3]) 
    max_stack_size = 1000 if (len(sys.argv) <= 4) else int(sys.argv[4])
    main(sys.argv[1],sys.argv[2])