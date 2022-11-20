import os
import random

INPUT_FORMAT = "input_{}.txt"
OUTPUT_FORMAT = "output_{}.txt"
TEST_NUM_EACH = 10

# Small test generator
for ITH in range(TEST_NUM_EACH):
    n = random.randint(50, 1000)
    m = random.randint(5, 10)
    input_file = INPUT_FORMAT.format(str(ITH))
    output_file = OUTPUT_FORMAT.format(str(ITH))
    with open(input_file, "w") as file:
        print(random.randint(1000, 250000), file=file)
        print(m, file=file)
        w = []
        for _ in range(n):
            w.append(str(random.randint(20, 250)))
        print(', '.join(w), file=file)
        v = []
        for _ in range(n):
            v.append(str(random.randint(20, 250)))
        print(', '.join(v), file=file)
        c = []
        for _ in range(n):
            c.append(str(random.randint(1, m)))
        print(', '.join(c), file=file)
    os.system("python algorithm_4.py {} {}".format(input_file, output_file))


# Large test generator
