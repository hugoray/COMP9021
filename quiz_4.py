# COMP9021 19T3 - Rachid Hamadi
# Quiz 4 *** Due Thursday Week 5
#
# Prompts the user for an arity (a natural number) n and a word.
# Call symbol a word consisting of nothing but alphabetic characters
# and underscores.
# Checks that the word is valid, in that it satisfies the following
# inductive definition:
# - a symbol, with spaces allowed at both ends, is a valid word;
# - a word of the form s(w_1,...,w_n) with s denoting a symbol and
#   w_1, ..., w_n denoting valid words, with spaces allowed at both ends
#   and around parentheses and commas, is a valid word.


import sys


def is_valid(word, arity):
    if word.find("("):
        a = word.find("(")
        for i in range(a):
            if not word[i].isalpha() and word[i] not in ['_']:
                return False
    # eliminate the blanks in the word
    word_no_blanks = word.replace(" ", "")
    # print(word_no_blanks)
    count_left_parentheses = []
    count_right_parentheses = []
    count_comma = []
    word_element = ''
    for i in range(len(word_no_blanks)):
        if word_no_blanks[i] == "(":
            count_left_parentheses.append(i)
        elif word_no_blanks[i] == ",":
            count_comma.append(i)
        elif word_no_blanks[i] == ")":
            count_right_parentheses.append(i)
        else:
            word_element += word_no_blanks[i]

    for i in word_element:
        if not i.isalpha() and i not in ['_']:
            return False
    # print(count_right_parentheses)
    # print(count_left_parentheses)
    # print(count_comma)
    # check when arity is 0, the word has any parentheses or underline or number
    if arity == 0:
        for i in range(len(word_no_blanks)):
            if not word_no_blanks[i].isalpha() and word_no_blanks[i] not in ['_']:
                return False
        if word.find("(") == -1 and word.find(")") == -1:
            return True
        else:
            return False

    elif arity > 0:
        # check the left character of all left parentheses is alphabet
        for item in count_left_parentheses:
            if not word_no_blanks[item - 1].isalpha() and word_no_blanks[item-1] not in ['_']:
                return False
        # check whether there's right parentheses on the right side of comma, if yes, return false
        for item in count_comma:
            if (item + 1) in count_right_parentheses:
                return False
        # check whether there's left parentheses just beside the right parentheses
        for item in count_right_parentheses:
            if (item - 1) in count_left_parentheses:
                return False
        # check whether right parentheses is at the last digit
        if (len(word_no_blanks) - 1) not in count_right_parentheses:
            return False
        # check whether the NO.left_par = NO.right_par
        if (len(count_left_parentheses) + len(count_right_parentheses)) % 2 == 1 or len(count_right_parentheses) != len(count_left_parentheses):
            return False
        # check whether there is comma when arity is 1, if yes ,return false
        if arity == 1:
            if len(count_comma) != 0:
                return False
            else:
                return True
        # check whether the left parentheses is at the first of all three parameters
        if count_left_parentheses[0] > count_right_parentheses[0] or count_left_parentheses[0] > count_comma[0]:
            return False
        if len(count_left_parentheses) == len(count_comma) / (arity - 1):
            return True
        else:
            return False

    # REPLACE THE RETURN STATEMENT ABOVE WITH YOUR CODE

try:
    arity = int(input('Input an arity : '))
    if arity < 0:
        raise ValueError
except ValueError:
    print('Incorrect arity, giving up...')
    sys.exit()
word = input('Input a word: ')
if is_valid(word, arity):
    print('The word is valid.')
else:
    print('The word is invalid.')

