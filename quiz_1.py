# COMP9021 19T3 - Rachid Hamadi
# Quiz 1 *** Due Thursday Week 2


import sys
from random import seed, randrange


try:
    arg_for_seed, upper_bound = (abs(int(x)) + 1 for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
mapping = {}
for i in range(1, upper_bound):
    r = randrange(-upper_bound // 2, upper_bound)
    if r > 0:
        mapping[i] = r
print('\nThe generated mapping is:')
print('  ', mapping)

mapping_as_a_list = []
one_to_one_part_of_mapping = {}
nonkeys = []

# INSERT YOUR CODE HERE

mapping_as_a_list.append(None)
one_to_one_list = []
print()
print('The mappings\'s so-called "keys" make up a set whose number of elements is %d.'%(len(mapping)))
print('\nThe list of integers between 1 and', upper_bound - 1, 'that are not keys of the mapping is:')
for i in range(1,upper_bound):
    if i in mapping:
        mapping_as_a_list.append(mapping[i])
    else:
        nonkeys.append(i)
        nonkeys.sort()
        mapping_as_a_list.append(None)

print('  ', nonkeys)
print('\nRepresented as a list, the mapping is:')
print('  ', mapping_as_a_list)
# Recreating the dictionary, inserting keys from smallest to largest,
# to make sure the dictionary is printed out with keys from smallest to largest.
for x in mapping_as_a_list:
    if mapping_as_a_list.count(x) == 1:
        one_to_one_list.append(x)

for j in one_to_one_list:
    for k in mapping:
        if j == mapping[k]:
            one_to_one_part_of_mapping[k] = j


one_to_one_part_of_mapping = {key: one_to_one_part_of_mapping[key]
                                      for key in sorted(one_to_one_part_of_mapping)
                             }
print('\nThe one-to-one part of the mapping is:')
print('  ', one_to_one_part_of_mapping)


