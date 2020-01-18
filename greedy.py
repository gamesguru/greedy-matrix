#!/usr/bin/env python3

import csv

# Get pairs and singles
nums = set()
pairs = set()

print("Read in CSV")
# Read in
with open("small.csv") as f:
    reader = csv.reader(f)
    for row in reader:
        i = int(row[2])
        j = int(row[3])
        pairs.add((i, j))
        nums.add(i)
        nums.add(j)

# Find max
n = max(nums)
print(n)

print("Prune compliments")
# Remove compliments
for i in range(0, n):
    for j in range(0, n):
        pair = (i, j)
        anti_pair = (j, i)
        if not pair in pairs and anti_pair in pairs:
            pairs.remove(anti_pair)

print(len(pairs))

matches = {0: 0}
# Apply Greedy
while len(matches) > max(matches.values()):
    matches = {}

    print(f"\nIterate..")
    for pair in pairs:
        k = pair[0]
        v = pair[1]
        if not k in matches:
            matches[k] = 0
        matches[k] += 1
    print(f'{len(matches)} stop remaining')
    # print("Find least paired")
    k = min(matches, key=matches.get)
    v = matches[k]
    floor = v
    # print(f"Floor: {floor}")
    while matches[k] == floor:
        print(f"  del {k}->{matches[k]}")
        del matches[k]
        k = min(matches, key=matches.get)
        v = matches[k]
    print(f'..done!  {len(matches)} remaining')

print(list(matches.keys()))
