import ast
import time

def setting_keys(dic, user, value):
    if user not in dic.keys():
        dic[user] = []
    dic[user].append(value)
    return dic

def convert(cliques):
    dic_of_users = {}
    for c in cliques:
        user1 = c[0]
        user2 = c[1]
        dic_of_users = setting_keys(dic_of_users, user1, user2)
        dic_of_users = setting_keys(dic_of_users, user2, user1)
    return dic_of_users

def find_clique(analisado, clique, dic, excluded):
    for i in range(len(clique) - 1, -1, -1):
        if clique[i] not in dic[analisado]:
            excluded.append(analisado)
            return clique, excluded
    clique.append(analisado)
    excluded.append(analisado)
    choosen = None
    for i in dic[analisado]:
        if i not in excluded:
            choosen = i
            break
    if choosen is not None:
        clique, excluded = find_clique(choosen, clique, dic, excluded)
    return clique, excluded

def max_clique(dic, degrees):
    max_clique = []
    flag = 0 # para controlar se ele passou do primeiro pivo
    for u in degrees:
        excluded = []
        user = u[0]
        for i in dic[user]:
            excluded = [user]
            if i not in excluded:
                clique = [user]
                clique, excluded = find_clique(i, clique, dic, excluded)
                if len(max_clique) == 0:
                    max_clique = clique
                else:
                    if flag == 0:
                        # ainda está no primeiro
                        if len(max_clique) < len(clique):
                            max_clique = clique
                    else:
                        if len(max_clique) < len(clique):
                            max_clique = clique
                            flag = 2
                        else:
                            flag = -1
                            break
        if flag == -1:
            break
        flag = 1
    return max_clique

inicio = time.time()

lineList = ''
with open('cliques_phb.json') as f:
    for line in f:
        lineList += line
clique = ast.literal_eval(lineList)

dic_of_users = convert(clique)

users = lineList.replace('[', '')
users = users.replace(']', '')
users = ast.literal_eval(users)
users = set(users)

## Pivoteamento

cont = 0
dict_users = []
degrees = []

for user in users:
    cont = 0
    for tuple in clique:
        if user in tuple:
            cont += 1
            dict_users.append([user, cont])

for user in users:
    max_degree = 0
    for list_in in dict_users:
        if user == list_in[0]:
            max_degree = max(max_degree, list_in[1])
    degrees.append([user, max_degree])
degrees.sort(key=lambda x: x[1], reverse=True)

max_clique = set(max_clique(dic_of_users, degrees))

print(max_clique)
fim = time.time()
print(fim - inicio)
