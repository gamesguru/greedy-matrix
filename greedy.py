#!/usr/bin/env python3

import sys
import csv


def main(args):

    # Get pairs and singles
    nums = set()
    pairs = set()

    if len(args) > 0:
        input_file = args[0]
        o_index = int(args[1])
        d_index = int(args[2])
    else:
        input_file = 'resources/300,300.csv'
        o_index = 0
        d_index = 1

    # Read in
    print("Read in CSV")
    with open(input_file) as f:
        reader = csv.reader(f)
        for row in reader:
            i = int(row[o_index])
            j = int(row[d_index])
            pairs.add((i, j))
            nums.add(i)
            nums.add(j)

    # Find max
    n = len(nums)
    m = max(nums)
    print(f'''Pre-pruning
    Span:  {n}
    Max:   {m}
    Miss:  {[x for x in range(0, m) if not x in nums]}
    Pairs: {len(pairs)}
    ''')
    print(f"Num stops: {n}\n")

    # Remove compliments
    print("Prune compliments")
    for i in nums:
        for j in nums:
            pair = (i, j)
            anti_pair = (j, i)
            if not pair in pairs and anti_pair in pairs:
                pairs.remove(anti_pair)

    print(f"Post pruning: {len(pairs)} entries")
    print(
        """
--------------------
Begin GREEDY algo
--------------------
    """
    )

    # Init dict
    matches = {i: 0 for i in nums}

    # Apply Greedy
    loops = 1
    while True:

        # Restart tallies
        print(f"\n\n==> ITERATION #{loops}")
        matches = {i: 0 for i in matches.keys()}

        # Tallies
        for i, j in pairs:
            if i in matches and j in matches:
                matches[i] += 1
        print(f"{len(matches)} stops remaining")

        k = min(matches, key=matches.get)
        v = matches[k]
        floor = v

        # Break if square
        if all(x == floor for x in matches.values()):
            print(
                f"""
----------------------------------
DONE: all have {floor} matches!
----------------------------------
    """
            )
            break

        # Greedy selection
        print("Prune weakest links")
        while matches[k] == floor:
            print(f"  del {k}  ({matches[k]} occurances)")
            del matches[k]
            k = min(matches, key=matches.get)
            v = matches[k]

        # Continue
        loops += 1

    solution = set(matches.keys())
    print(solution)

    # Stream output
    print('\n==> Streaming new filtered CSV')
    with open(args[0].replace('.csv', '.filtered.csv'), 'w+') as csv_out:
        writer = csv.writer(csv_out)

        # Read in
        with open(input_file) as csv_in:
            reader = csv.reader(csv_in)

            for row in reader:
                i = int(row[o_index])
                j = int(row[d_index])
                # Add only members of the square solution
                if i in solution and j in solution and i != j:
                    writer.writerow(row)


# Main script executable
if __name__ == '__main__':
    main(sys.argv[1:])
