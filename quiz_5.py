# COMP9021 19T3 - Rachid Hamadi
# Quiz 5 *** Due Thursday Week 7
#
# Implements a function that, based on the encoding of
# a single strictly positive integer that in base 2,
# reads as b_1 ... b_n, as b_1b_1 ... b_nb_n, encodes
# a sequence of strictly positive integers N_1 ... N_k
# with k >= 1 as N_1* 0 ... 0 N_k* where for all 0 < i <= k,
# N_i* is the encoding of N_i.
#
# Implements a function to decode a positive integer N
# into a sequence of (one or more) strictly positive
# integers according to the previous encoding scheme,
# or return None in case N does not encode such a sequence.


import sys


def encode(list_of_integers):
    result = ''
    list_of_binarys = []
    list_of_binarys_output = []
    # input is list
    for item in list_of_integers:
        list_of_binarys.append(bin(item)[2:])
    for item in list_of_binarys:
        val = ""
        for i in range(len(item)):
            val += item[i]*2
        list_of_binarys_output.append(val)
    if len(list_of_binarys_output) == 1:
        return int(list_of_binarys_output[0],2)
    for i in range(len(list_of_binarys_output)-1):
        result += list_of_binarys_output[i]
        if list_of_binarys_output[i+1].startswith('1'):
            list_of_binarys_output[i+1] = '0' + list_of_binarys_output[i+1]
        else:
            list_of_binarys_output[i+1] = '1' + list_of_binarys_output[i+1]
    result += list_of_binarys_output[-1]
    return int(str(result),2)

def decode(integer):
    binary = str(bin(integer)[2:])
    binary_list = []
    binary_list_sort = []
    index = []
    binary_list_sort_2 = []
    output = []
    for item in binary:
        binary_list.append(item)
    if len(binary_list) <= 1:
        return None
    else:
        if binary_list[-1] != binary_list[-2] or binary_list[0] != binary_list[1]:
            return None
        else:
            num = 0
            while num < len(binary_list)-1:
                if binary_list[num] == binary_list[num+1]:
                    binary_list_sort.append(binary_list[num])
                    num += 2
                else:
                    if binary_list[num+1] == binary_list[num+2]:
                        binary_list_sort.append('')
                        num += 1
                    else:
                        return None
        for i in range(len(binary_list_sort)):
            if binary_list_sort[i] == '':
                index.append(i)
        if index == []:
            result = ''
            for i in range(len(binary_list_sort)):
                result += binary_list_sort[i]
            output = [int(result,2)]
        else:
            if len(index) == 1:
                result = ''
                for item in binary_list_sort[:index[0]]:
                    result += item
                binary_list_sort_2.append(result)

                result = ''
                for item in binary_list_sort[index[0]+1:]:
                    result += item
                binary_list_sort_2.append(result)

            else:
                for i in range(len(index)):
                    if i == 0:
                        result = ''
                        for item in binary_list_sort[0:index[i]]:
                            result += item
                        binary_list_sort_2.append(result)
                    elif i == len(index) - 1:
                        result = ''
                        for item in binary_list_sort[index[i-1]+1:index[i]]:
                            result += item
                        binary_list_sort_2.append(result)
                        result = ''
                        for item in binary_list_sort[index[i]+1:]:
                            result += item
                        binary_list_sort_2.append(result)
                    elif 0 < i < len(index) - 1:
                        result = ''
                        for item in binary_list_sort[index[i-1]+1:index[i]]:
                            result += item
                        binary_list_sort_2.append(result)

            for item in binary_list_sort_2:
                output.append(int(item,2))
        return output

    # REPLACE pass ABOVE WITH YOUR CODE


# We assume that user input is valid. No need to check
# for validity, nor to take action in case it is invalid.
print('Input either a strictly positive integer')
the_input = eval(input('or a nonempty list of strictly positive integers: '))
if type(the_input) is int:
    print('  In base 2,', the_input, 'reads as', bin(the_input)[2 :])
    decoding = decode(the_input)
    if decoding is None:
        print('Incorrect encoding!')
    else:
        print('  It encodes: ', decode(the_input))
else:
    print('  In base 2,', the_input, 'reads as',
          f'[{", ".join(bin(e)[2: ] for e in the_input)}]'
         )
    print('  It is encoded by', encode(the_input))
