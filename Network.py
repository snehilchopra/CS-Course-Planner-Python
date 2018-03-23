import csv
import networkx as nx

data=dict()

with open('CSData.csv', 'r') as dataread:
    reader= csv.reader(dataread)
    for row in reader:
        data[row[0].split(":")[0]]=row

networkprereqs = nx.DiGraph()
networksimilarity = nx.Graph()

def add_weight(x1, x2, w):
    if networksimilarity.number_of_edges(x1, x2)>=1:
        networksimilarity[x1][x2]['weight']+=w   
    if (networksimilarity.number_of_edges(x2, x1) == 0):
        networksimilarity.add_edge(x2,x1,weight=w)
        
for i in data.keys():
    networkprereqs.add_node(i)
    networksimilarity.add_node(i)
    for p in data[i][6][2:-2].split("', '"):
        if p.split(" ")[0]=='CS':
            networkprereqs.add_edge(p,i)

for j1 in data.keys():
    profj1 = data[j1][5][2:-2].split("', '")
    for j2 in list(data.keys())[list(data.keys()).index(j1):]: 
        profj2 = data[j2][5][2:-2].split("', '")
        prof = list(set(profj1).intersection(profj2))
        if prof != [] and prof != ['N/A']:
            add_weight(j1, j2, .1)

for k1 in data.keys():
    topick1 = data[k1][7][2:-2].split("', '")
    for k2 in list(data.keys())[list(data.keys()).index(k1):]: 
        topick2 = data[k2][7][2:-2].split("', '")
        topic = list(set(topick1).intersection(topick2))
        if topic != [] and topic != ['N/A']:
            add_weight(k1, k2, .75)
for i in data.keys():
    print(list(networksimilarity.neighbors(i)))
           
taken = int(input('enter number of credit hours this semester:'))
a =int(input('enter number of classes'))
classes = {}
for i in range(a):
    c='CS ' + str(input("enter class number:"))
    gpa = str(input('enter letter grade:')).upper()
    classes[c]=gpa
print(classes)
p={}
q=[]              
for j in classes.keys():
    for key in network.adj[j]:
        if key not in classes.keys():
            if key not in p:
                p[key]=network.adj[j][key]['weight']
            else:
                p[key]+=network.adj[j][key]['weight']
for key,value in p.items():
    if value>:    
        q.append([key,value])

print(q)
