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

max_clique = []

def find_anothers(usr, dic, clique):
    for i in range(len(clique) - 1, -1, -1):
        if clique[i] not in dic[usr]:
            return clique
    clique.append(usr)
    for u in dic[usr]:
        if u not in clique:
            clique = find_anothers(u, dic, clique)
    return clique

for u in dic_of_users.keys():
    for u2 in dic_of_users[u]:
        clique = [u]
        clique = find_anothers(u2, dic_of_users, clique)
        print(clique)
        if len(clique) > len(max_clique):
            max_clique = clique

print(max_clique)
fim = time.time()
print(fim - inicio)
