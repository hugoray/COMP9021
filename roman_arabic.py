from collections import Counter
def check_answer():
    answer = input("How can I help you? ")
    # set function for converting just integers
    def condition_one(para):
        Alist = []
        val = 0
        dict_arab = {0 : ("","I","II","III","IV","V","VI","VII","VIII","IX"),
                     1 : ("","X","XX","XXX","XL","L","LX","LXX","LXXX","XC"),
                     2 : ("","C","CC","CCC","CD","D","DC","DCC","DCCC","CM"),
                     3 : ("","M","MM","MMM")}
        dict_roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        if para.isalpha():
            for i in range(len(para)):
                Alist.append(para[i])
            dict_save = Counter(Alist)
            for key in dict_save:
                if key in ['I','X','C','M']:
                    if dict_save[key] > 4:
                        return 'Hey, ask me something that\'s not impossible to do!'
                    elif dict_save[key] == 4:
                        if Alist[Alist.index(key)+3] == key:
                            return 'Hey, ask me something that\'s not impossible to do!'

                elif key in ['V','L','D']:
                    if dict_save[key] > 1:
                        return 'Hey, ask me something that\'s not impossible to do!'
                else:
                    return 'Hey, ask me something that\'s not impossible to do!'

            for i in range(len(Alist)-1):
                val += dict_roman[Alist[i]]
                if Alist[i] == 'I':
                    if Alist[i+1] == 'V' or Alist[i+1] == 'X':
                        val -= 2*dict_roman[Alist[i]]
                elif Alist[i] == 'X':
                    if Alist[i+1] == 'L' or Alist[i+1] == 'C':
                        val -= 2*dict_roman[Alist[i]]
                elif Alist[i] == 'C':
                    if Alist[i+1] == 'D' or Alist[i+1] == 'M':
                        val -= 2*dict_roman[Alist[i]]
            val += dict_roman[Alist[len(Alist)-1]]

            val_new = ''
            Alist = []
            Alist.append(dict_arab[3][val // 1000 % 10])
            Alist.append(dict_arab[2][val // 100 % 10])
            Alist.append(dict_arab[1][val // 10 % 10])
            Alist.append(dict_arab[0][val % 10])
            for item in Alist:
                val_new += item
            if para == val_new:
                return "Sure! It is " + str(val)
            else:
                return 'Hey, ask me something that\'s not impossible to do!'

        elif para.isdigit():
            if para[0] == '0':
                return 'Hey, ask me something that\'s not impossible to do!'
            else:
                num = int(para)
                if num > 3999 or num < 1:
                    return 'Hey, ask me something that\'s not impossible to do!'
                else:
                    val = ''
                    Alist = []
                    Alist.append(dict_arab[3][num//1000%10])
                    Alist.append(dict_arab[2][num//100%10])
                    Alist.append(dict_arab[1][num//10%10])
                    Alist.append(dict_arab[0][num % 10])
                    for item in Alist:
                        val += item
                    return "Sure! It is " + val

    # set function for converting numbers using
    def condition_two(a,b):
        list_a = []
        list_b = []
        list_b_num = []
        if ' ' in b:
            return "I don't get what you want, sorry mate!"

        if not b.isalpha():
            return 'Hey, ask me something that\'s not impossible to do!'
        else:
            for i in b:
                list_b.append(i)
            for item in list_b:
                if list_b.count(item) > 1:
                    return 'Hey, ask me something that\'s not impossible to do!'
            list_b.reverse()
            # convert the b part to a dict which contains key and value
            para = 0
            while para < len(list_b):
                ac = 1*10**(para//2)
                bc = 5*10**((para-1)//2)
                if para % 2 == 0:
                    list_b_num.append(ac)
                elif para % 2 == 1:
                    list_b_num.append(bc)
                para += 1
            dict_two = dict(zip(list_b , list_b_num))

        if a.isalpha():
            if len(a) < 5:
                if b[-1] in a:
                    if a[-1] == b[0] and a[-2] != b[1]:
                        return 'Hey, ask me something that\'s not impossible to do!'
            val = 0
            for i in a:
                list_a.append(i)
            for item in list_a:
                if not dict_two.__contains__(item):
                    return 'Hey, ask me something that\'s not impossible to do!'
                else:
                    # if item is at the even digit, it should appear at most 3 times
                    if list_b.index(item) % 2 == 0:
                        if list_a.count(item) > 3:
                            return 'Hey, ask me something that\'s not impossible to do!'

                    # if item is at the odd digit, it should appear at most 1 time
                    elif list_b.index(item) % 2 == 1:
                        if list_a.count(item) > 1:
                            return 'Hey, ask me something that\'s not impossible to do!'

                    val += dict_two[item]

            # 比较b表下偶数位在a表中的后一位是否为b表下的后两位，若是，减去两倍b表值
            for i in range(len(list_a)-1):
                if list_b.index(list_a[i]) % 2 == 0 and (list_b.index(list_a[i]) + 2) < len(list_b):
                    if list_a[i + 1] == list_b[list_b.index(list_a[i]) + 1] or list_a[i + 1] == list_b[list_b.index(list_a[i]) + 2]:
                        val -= 2 * dict_two[list_a[i]]
            if val == 6:
                val = 4
            return "Sure! It is " + str(val)

        elif a.isdigit():
            Alist = []
            val = ''
            for item in a:
                Alist.append(int(item))
            if 2*len(Alist) > len(list_b):
                return 'Hey, ask me something that\'s not impossible to do!'
            # 当元素小于4时，该数乘以其位数对应的；为4时，对应位加后一位；为5到8时，对应位后一位加对应位乘
            for i in range(len(Alist)):
                if Alist[i] < 4:
                    val += Alist[i]*list_b[2*(len(Alist)-1-i)]
                elif Alist[i] == 4:
                    val += list_b[2*(len(Alist)-1-i)] + list_b[2*(len(Alist)-1-i)+1]
                elif 5 <= Alist[i] < 9:
                    val += list_b[2*(len(Alist)-1-i)+1] + (Alist[i]-5)*list_b[2*(len(Alist)-1-i)]
                elif Alist[i] == 9:
                    val += list_b[2*(len(Alist)-1-i)] + list_b[2*(len(Alist)-1-i)+2]

            return "Sure! It is " + str(val)
        
        else:
             return "I don't get what you want, sorry mate!"
         
    def condition_three(para):
        # set a new funciton to get the index of string
        def get_index(string):
            return [string.index(i) for i in string]

        # set a dict which contains 1-100 num and val(in index)
        row = ['','I','II','III','IV','V','VI','VII','VIII','IX']
        column = ['','X','XX','XXX','XL','L','LX','LXX','LXXX','XC']
        list_new = []
        list_new_val = []

        #if len(para) < 3:
        #    if get_index(para) not in list_new_val:
        #        return 'Hey, ask me something that\'s not impossible to do!'

        for i in range(10):
            for j in range(10):
                combin = column[i] + row[j]
                list_new.append(combin)

        for item in list_new:
            list_new_val.append(get_index(item))

        cur = (len(para) - 1)
        pre = 0
        list_para = []
        list_para_sort = []
        while True:
            if pre != len(para)-1:
                if para[pre] == para[cur]:
                    list_para.append(para[pre:cur+1])
                    if cur != len(para) -1:
                        pre = cur + 1
                    else:
                        pre = cur
                    cur = len(para) - 1
                else:
                    cur -= 1
            else:
                if para.index(para[pre]) == pre:
                    list_para.append(para[pre])
                break
        list_para.reverse()
        num = 0
        pre = ''
        while True:
            cur = list_para[num]
            combin = cur + pre
            if get_index(combin) in list_new_val:
                pre = combin
                num += 1
            else:
                if get_index(pre) in list_new_val and pre !='':
                    list_para_sort.append(get_index(pre))
                    pre = ''
                    continue
                else:
                    return 'Hey, ask me something that\'s not impossible to do!'
            if num == len(list_para) and get_index(pre) in list_new_val:
                list_para_sort.append(get_index(pre))
                break

        list_para_sort.reverse()
        num_output = ''
        val_list = []
        for item in list_para_sort:
            num_output += str(list_new_val.index(item))
            val_list.append(list_new_val.index(item))

        length_list = []
        for item in list_para_sort:
            length_list.append(len(item))
        word_split = []
        sum_pre = 0
        sum = 0
        for item in length_list:
            sum_pre = sum
            sum += item
            if sum_pre == 0:
                word_split.append(para[:item])
            else:
                word_split.append(para[sum_pre:sum])

        model_dict = {'L':50,'X':10,'V':5,'I':1}
        model_list = []
        for item in val_list:
            model_list.append(list_new[item])

        #model_num_list = []
        dict_norm = {}
        sum = 0
        for item in val_list:
            sum += len(str(item))

        for i in range(len(model_list)):
            #val = ''
            sum -= len(str(val_list[i]))
            for j in range(len(model_list[i])):
                dict_norm[model_dict[model_list[i][j]]*10**sum] = word_split[i][j]

        max_key = max(dict_norm.keys())
        str_output = ''
        while max_key >0:
            if max_key in dict_norm.keys():
                str_output += dict_norm[max_key]
            else:
                str_output += '_'
            if str(max_key)[0] == '1':
                max_key = max_key // 2
            else:
                max_key = max_key // 5

        return f'Sure! It is {num_output} using {str_output}'

    if len(answer) < 15:
        return "I don't get what you want, sorry mate!"
    elif answer[:15] != "Please convert ":
        return "I don't get what you want, sorry mate!"
    else:
        input_answer = answer[15:]
        # check the specific situation of three cases
        if input_answer.find(" using ") != -1:
            des = input_answer.find(" using ")
            a = input_answer[:des]
            b = input_answer[des + 7:]
            return condition_two(a,b)
        elif input_answer[-10:] == " minimally":
            para = input_answer[:-10]
            for i in para:
                if not i.isalpha():
                    return 'Hey, ask me something that\'s not impossible to do!'
            return condition_three(para)
        else:
            para = input_answer[:]
            if para.isdigit() or para.isalpha():
                return condition_one(para)
            else:
                return "I don't get what you want, sorry mate!"
print(check_answer())


