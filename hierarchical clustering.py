from __future__ import division
import os.path
import numpy as np
import collections


#there are two ways to flatten
#1
def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el


#2
def flatten(container):
    for i in container:
        if isinstance(i, (list,tuple)):
            for j in flatten(i):
                yield j
        else:
            yield i


filename = "rosalind_ba8e.txt"
enclosed_folder = "/Users/Unname/Dropbox/UCLA Academic/2016-2017 Spring/CM224 - Computational Genetics/rosalind"
full_path = os.path.join(enclosed_folder,filename)



with open(full_path) as input_data:
    temp = input_data.readlines()
    n = int(temp.pop(0))
    matrix = [x.split(" ") for x in temp]
    for i in range(n):
        for j in range(n):
            matrix[i][j] = float(matrix[i][j])
    input_data.close()


# def get_min_nonzero(dictvalues):
#     nonzerodictvalues = filter(lambda a: a != 0.0, dictvalues)  # filter non zero values
#     min_value = min(nonzerodictvalues)
#     return min_value

dict = {}
for i in range(1, n + 1):
    for j in range(1, n + 1):
        if i < j and i != j:
            dict[(str(i), str(j))] = matrix[i - 1][j - 1]
        #dict["("+ ",".join ([str(i), str(j)]) + ")"] = matrix[i-1][j-1]



initial_dict = dict.copy()
initial_nodes = [str(x) for x in range(1,n+1)]
remaining_nodes = initial_nodes.copy()
current_nodes = remaining_nodes.copy()

new_nodes = []

while True:


    if len(current_nodes) == 1:
        break

    dictvalues = dict.values()
    min_value = min(dictvalues)
    min_key = [k for k, v in dict.items() if v == min_value][0]


    new_nodes.append(min_key)


    temp = []
    for x in current_nodes:
        if str(x) == x:
            if not x in min_key:
                temp.append(x)
        else:
            if not set(x) <= set(min_key):
                temp.append(x)

    current_nodes = temp.copy()

    to_be_removed = []

    for key in dict.keys():
        for i in key:
            if i in min_key and key not in to_be_removed:
                to_be_removed.append(key)

    for x in to_be_removed:
        del dict[x]

    for x in current_nodes:
        to_be_averaged = []
        if str(x) == x:
            for j in min_key:
                try:
                    to_be_averaged.append(initial_dict[(x, j)])
                except KeyError:
                    to_be_averaged.append(initial_dict[(j, x)])
        else:
            for i in x:
                for j in min_key:
                    try:
                        to_be_averaged.append(initial_dict[(i, j)])
                    except KeyError:
                        to_be_averaged.append(initial_dict[(j, i)])

        dict[tuple(list(flatten((x, min_key))))] = np.mean(to_be_averaged)


    current_nodes.append(min_key)
    print(current_nodes)

print('\n'.join([' '.join(map(str, x)) for x in new_nodes]))
