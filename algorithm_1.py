import sys

class Item:
  def __init__(self, w, v, c):
    self.w = w
    self.v = v
    self.c = c


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
            items.append(Item(w[i], v[i], c[i]))


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
            if (item.w + weight <= W):
                f += item.v
                w += item.w
            else:
                f += item.v * ((W - w)/item.w)
                break
    return f


def process():
    global ans, W, m
    ans = [0, 0]
    for s in range((1 << n) - 1):
        v = 0
        w = 0
        setOfClasses = set()
        for i in range(n):
            if (s & (1 << i)):
                setOfClasses.add(items[i].c)
                v += items[i].v
                w += items[i].w
        if (w > W or len(setOfClasses) != m):
            continue
        if (ans[0] < v):
            ans = [v, s]


def commit(output_path):
    global ans, items
    with open(output_path, "w") as file:
        print(ans[0], file=file) 
        output_str = ""
        for i in range(n):
            if (ans[1] & (1 << i)):
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
        print('usage:\talgorithm_1.py <input_file> <output_file>')
        sys.exit(0)
    main(sys.argv[1],sys.argv[2])