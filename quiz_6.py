# COMP9021 19T3 - Rachid Hamadi
# Quiz 6 *** Due Thursday Week 8
#
# Randomly fills an array of size 10x10 with 0s and 1s, and outputs the size of
# the largest parallelogram with horizontal sides.
# A parallelogram consists of a line with at least 2 consecutive 1s,
# with below at least one line with the same number of consecutive 1s,
# all those lines being aligned vertically in which case the parallelogram
# is actually a rectangle, e.g.
#      111
#      111
#      111
#      111
# or consecutive lines move to the left by one position, e.g.
#      111
#     111
#    111
#   111
# or consecutive lines move to the right by one position, e.g.
#      111
#       111
#        111
#         111


from random import seed, randrange
import sys


dim = 10


def display_grid():
    for row in grid:
        print('   ', *row)


def grid_right():
    grid_new = []
    for item in grid:
        grid_new.append(item)
    for i in range(len(grid_new)):
        grid_new[i] = [0]*i + grid_new[i] + [0]*(len(grid_new)-1-i)
    return grid_new

def grid_left():
    grid_new = []
    for item in grid:
        grid_new.append(item)
    for i in range(len(grid_new)):
        grid_new[i] = [0]*(len(grid_new)-1-i) + grid_new[i] + [0]*i
    return grid_new

def size_of_largest_parallelogram():
   Compare_list = []
   def find_the_largest_rectangle(grid):
       heights = [0] * (len(grid[0]))
       Alist = []
       for row in grid:
           for i in range(len(grid[0])):
               if row[i] == 1:
                   heights[i] = heights[i] + 1
               else:
                   heights[i] = 0

           res = 0
           stack = []
           heights.append(-1)
           for i in range(len(heights)):
               current = heights[i]
               while stack != [] and current <= heights[stack[-1]]:
                   h = heights[stack.pop()]
                   if h == 1:
                       h = 0
                   w = i if len(stack) == 0 else i -stack[-1] -1
                   if w == 1:
                       w = 0
                   res =max(res, h * w)
               stack.append(i)
           Alist.append(res)
       return max(Alist)

   Compare_list.append(find_the_largest_rectangle(grid))
   Compare_list.append(find_the_largest_rectangle(grid_right()))
   Compare_list.append(find_the_largest_rectangle(grid_left()))
   return max(Compare_list)

    # REPLACE PASS ABOVE WITH YOUR CODE


# POSSIBLY DEFINE OTHER FUNCTIONS


try:
    
    for_seed, density = (int(x) for x in input('Enter two integers, the second '
                                               'one being strictly positive: '
                                              ).split()
                    )
    if density <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(for_seed)
grid = [[int(randrange(density) != 0) for _ in range(dim)]
            for _ in range(dim)
       ]
print('Here is the grid that has been generated:')
display_grid()
size = size_of_largest_parallelogram()
if size:
    print('The largest parallelogram with horizontal sides '
          f'has a size of {size}.'
         )
else:
    print('There is no parallelogram with horizontal sides.')
