import csv
import time

import numpy as np


def matrix_from_matrix_csv(input_file):

    # Create matrix
    n = sum(1 for line in open(input_file))
    matrix = np.zeros((n, n), dtype=np.byte,)

    # Read in
    t0 = time.time()
    print("Read in CSV")
    with open(input_file) as f:
        reader = csv.reader(f)

        i = 0
        for line in reader:
            matrix[i] = line
            i += 1

    # Fill diag with ones
    np.fill_diagonal(matrix, 1)
    print(f"{time.time() - t0}s")

    return matrix


def matrix_from_rel_csv(input_file):

    # Get pairs and singles
    nums = set()
    pairs = set()

    # Index of o/d in CSV columns
    o_index = 0
    d_index = 1

    # Read in
    t0 = time.time()
    print("Read in CSV")
    with open(input_file) as f:
        reader = csv.reader(f)
        for row in reader:
            i = int(row[o_index])
            j = int(row[d_index])
            pairs.add((i, j))
            nums.add(i)
            nums.add(j)
    print(f"{time.time() - t0}s")

    # Find max
    n = len(nums)
    m = max(nums)
    print(
        f"""
Pre-pruning
    Span:  {n}
    Max:   {m}
    Miss:  {[x for x in range(0, m) if not x in nums]}
    Pairs: {len(pairs)}
    """
    )
    print(f"Num stops: {n}\n")

    # Remove compliments
    t0 = time.time()
    print("==> Prune compliments\n")
    for i in nums:
        for j in nums:
            pair = (i, j)
            anti_pair = (j, i)
            if not pair in pairs and anti_pair in pairs:
                pairs.remove(anti_pair)
    print(f"Post pruning: {len(pairs)} entries")
    print(f"{time.time() - t0}s")

    # Create the matrix
    t0 = time.time()
    print("\nDump into numpy matrix[][]")
    matrix = np.zeros((n, n), dtype=np.byte,)
    np.fill_diagonal(matrix, 1)

    for p in pairs:
        i = p[0]
        j = p[1]
        # Set cell True
        matrix[i][j] = 1
    del pairs
    print(f"{time.time() - t0}s")

    return matrix
