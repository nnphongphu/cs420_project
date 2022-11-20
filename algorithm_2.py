import sys

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
    global W, m, n, items
    items = []
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


def calF(state, value, weight):
    global W, m
    if (weight > W):
        return -1

    setOfClass = set()
    for i in range(n):
        if (state & (1 << i)):
            setOfClass.add(items[i].c)
    
    if (len(setOfClass) != m):
        return -1

    f = value
    w = weight
    for i, item in enumerate(items):
        if ((state & (1 << i)) == 0):
            if (item.w + w <= W):
                f += item.v
                w += item.w
            else:
                f += item.v * ((W - w)/item.w)
                break
    return f


def process():
    global bound, ans, W
    bound = -1
    q = []
    ans = [0, 0]
    q.append(Node(0, 0, 0, -1))
    visited = {}

    while (len(q)):
        at = q.pop(0)

        if (at.f < bound):
            continue
    
        for i in range(n):
            if ((at.s & (1 << i)) == 0 and items[i].w + at.w <= W):
                toS = at.s | (1 << i)
                toV = at.v + items[i].v
                toW = at.w + items[i].w
                if (visited.get(str(toS), False)):
                    continue

                visited[str(toS)] = True
                to = Node(toS, toV, toW, calF(toS, toV, toW))
                q.append(to)
                if (bound < to.f):
                    bound = to.f
                if (to.f > 0 and ans[0] < to.v):
                    ans = [to.v, to.s]


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
    if (len(sys.argv) != 3):
        print('usage:\talgorithm_2.py <input_file> <output_file>')
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])