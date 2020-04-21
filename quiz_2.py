# COMP9021 19T3 - Rachid Hamadi
# Quiz 2 *** Due Thursday Week 3


import sys
from random import seed, randrange
from pprint import pprint

try:
    arg_for_seed, upper_bound = (abs(int(x)) + 1 for x in input('Enter two integers: ').split())
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
mapping = {}
for i in range(1, upper_bound):
    r = randrange(-upper_bound // 8, upper_bound)
    if r > 0:
        mapping[i] = r
print('\nThe generated mapping is:')
print('  ', mapping)
# sorted() can take as argument a list, a dictionary, a set...
keys = sorted(mapping.keys())
print('\nThe keys are, from smallest to largest: ')
print('  ', keys)

cycles = []
reversed_dict_per_length = {}

# INSERT YOUR CODE HERE
# solution 1
newlist = keys[:]
for item in keys:
    path = []
    while item in newlist:
        newlist.remove(item)
        path.append(item)
        item = mapping[item]
        #  judge the value with the key at once
    if item in path and item == path[0]:
        cycles.append(path)
    else:
        # if not, put the element of path to the newlist
        newlist.extend(path)    # extend means add the (Alist)'s element to the bList


# solution 2(still in study)


Blist = []
for item in keys:
    Blist.append(mapping[item])

Blist.sort()

def get_key(value):
    return [k for k , v in mapping.items() if v == value]

reversed_dict_per_length = {}

for i in Blist:
    Clist = get_key(i)
    dic_val_key = {}
    dic_val_key[i] = Clist
    # if len(Clist) is in the reversed_dict, just update it to the existed one, else create a new key:value
    if len(Clist) not in reversed_dict_per_length:
        reversed_dict_per_length[len(Clist)]=(dic_val_key)
    else:
        reversed_dict_per_length[len(Clist)].update(dic_val_key)

print('\nProperly ordered, the cycles given by the mapping are: ')
print('  ', cycles)
print('\nThe (triply ordered) reversed dictionary per lengths is: ')
pprint(reversed_dict_per_length)

