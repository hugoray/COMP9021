# COMP9021 19T3 - Rachid Hamadi
# Quiz 3 *** Due Thursday Week 4


# Reading the number written in base 8 from right to left,
# keeping the leading 0's, if any:
# 0: move N     1: move NE    2: move E     3: move SE
# 4: move S     5: move SW    6: move W     7: move NW
#
# We start from a position that is the unique position
# where the switch is on.
#
# Moving to a position switches on to off, off to on there.

import sys

on = '\u26aa'
off = '\u26ab'
code = input('Enter a non-strictly negative integer: ').strip()
try:
    if code[0] == '-':
        raise ValueError
    int(code)
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
nb_of_leading_zeroes = 0
for i in range(len(code) - 1):
    if code[i] == '0':
        nb_of_leading_zeroes += 1
    else:
        break
print("Keeping leading 0's, if any, in base 8,", code, 'reads as',
      '0' * nb_of_leading_zeroes + f'{int(code):o}.'
     )
print()

# INSERT YOUR CODE HERE
# invert code into oct then to list
code_str = ('0' * nb_of_leading_zeroes + f'{int(code):o}')
Alist = []
for i in range(len(code_str)):
    Alist.append(int(code_str[i]))
Alist.reverse()
#print(Alist)

init_x, init_y = (0, 0)
mov_x, mov_y =(0,0)
Mov_list = [(init_x,init_y)]
Compare_list_x = []
Compare_list_y = []
for i in range(len(Alist)):
    # set the moving rule
    if Alist[i] == 0:
        mov_x, mov_y = (mov_x, mov_y + 1)
    elif Alist[i] == 1:
        mov_x, mov_y = (mov_x + 1, mov_y + 1)
    elif Alist[i] == 2:
        mov_x, mov_y = (mov_x + 1, mov_y)
    elif Alist[i] == 3:
        mov_x, mov_y = (mov_x + 1, mov_y - 1)
    elif Alist[i] == 4:
        mov_x, mov_y = (mov_x, mov_y - 1)
    elif Alist[i] == 5:
        mov_x, mov_y = (mov_x - 1, mov_y - 1)
    elif Alist[i] == 6:
        mov_x, mov_y = (mov_x - 1, mov_y)
    elif Alist[i] == 7:
        mov_x, mov_y = (mov_x - 1, mov_y + 1)

    # check if mov_pos is in the Mov_list
    if (mov_x,mov_y) in Mov_list:
        Mov_list.remove((mov_x,mov_y))

    else:
        Mov_list.append((mov_x,mov_y))

# sort out the largest and smallest item in Mov_list
if Mov_list != []:
    for item in Mov_list:
        Compare_list_x.append(item[0])
        Compare_list_y.append(item[1])

    Compare_list_x.sort()
    Compare_list_y.sort()
    #print(Mov_list)
    #print(Compare_list_y)
    #print(Compare_list_x)

    max_x = Compare_list_x[-1]
    min_x = Compare_list_x[0]
    max_y = Compare_list_y[-1]
    min_y = Compare_list_y[0]

    for y in reversed(range(min_y,max_y+1)):
        for x in range(min_x,max_x+1):
            if (x,y) in Mov_list:
                print(on,end="")
            else:
                print(off,end="")
        if y != min_y:
            print("\r")