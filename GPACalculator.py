import pandas as pd
import csv
import networkx as nx

data = dict()

with open('CSData.csv', 'r') as dataread:
    reader = csv.reader(dataread)
    for row in reader:
        data[row[0].split(":")[0]] = row

network = nx.DiGraph()

def add_weight(x1, x2, w):
    if network.number_of_edges(x1, x2) >= 1:
        network[x1][x2]['weight'] += w
    if network.number_of_edges(x2, x1) >= 1:
        network[x2][x1]['weight'] += w
    if (network.number_of_edges(x2, x1) == 0) & (network.number_of_edges(x1, x2) == 0):
        network.add_edge(x2, x1, weight=w)
        network.add_edge(x1, x2, weight=w)


def preprocess_data():
    # creates a pandas dataframe from grade distributions of classes from fall 2014 file
    class_data = []
    dist = {}

    with open("Fall_2014.csv", 'r') as f:
        f.readlines(1)  #skip header
        for row in f.readlines():
            row = row.strip("\n").split(",")
            class_data.append(row)

    for i in range(len(class_data)):
        if class_data[i][2] not in dist:
            init_gpa = float(class_data[i][-1].strip("\""))
            results = list(map(int, class_data[i][9:-1]))
            dist["CS " + str(class_data[i][2])] = results, init_gpa, 1
        else:
            results = list(map(int, class_data[i][9:-1]))
            temp = []
            accumulated_results, tot_gpa, tot_occurrences = dist[class_data[i][2]]

            for num in range(len(results)):
                temp.append(accumulated_results[num] + results[num])

            new_tot_gpa = (tot_gpa * tot_occurrences + float(class_data[i][-1].strip("\""))) / (tot_occurrences + 1)
            dist["CS " + str(class_data[i][2])] = temp, float("%.2f" % new_tot_gpa), (tot_occurrences + 1)

    dist_df = pd.DataFrame.from_dict(dist, orient='index')
    dist_df2 = pd.DataFrame(dist_df[0].values.tolist(), columns=['A+','A','A-','B+','B','B-','C+','C','C-','D+',
                                                                 'D','D-','E','F', ])

    dist_df2 = dist_df2.drop(['E'], axis=1)
    stdv = (dist_df2.std(axis=1))

    dist_df2["Class"] = dist.keys()
    #calculates average gpa and standard deviation in case we want z scores
    dist_df2['Average GPA'] = dist_df[1].values.tolist()
    dist_df2['stdv'] = stdv

    return dist_df2


def main():

    pre_reqs = {}
    for i in data.keys():
        network.add_node(i)
        for p in data[i][6][2:-2].split("', '"):
            temp = []
            if p.split(" ")[0] == "CS":
                network.add_edge(p,i, weight=1)
                temp.append(p)
                pre_reqs[i] = temp

    for k1 in data.keys():
        topick1 = data[k1][7][2:-2].split("', '")
        for k2 in list(data.keys())[list(data.keys()).index(k1):]:
            topick2 = data[k2][7][2:-2].split("', '")
            topic = list(set(topick1).intersection(topick2))
            if topic != [] and topic != ['N/A']:
                add_weight(k1, k2, .75)


    a = int(input('Enter number CS of classes taken previously: '))
    classes = {}
    for i in range(a):
        c = "CS " + str(input("Enter class number: "))
        gpa = str(input('Enter letter grade: ')).upper()
        classes[c] = gpa

    p = {}
    q = []

    for j in classes.keys():
        for key in network.adj[j]:
            if key not in classes.keys():
                if key not in p:
                    p[key] = network.adj[j][key]['weight']
                else:
                    p[key] += network.adj[j][key]['weight']
    for key, value in p.items():
        if value > 0:
            q.append([key, value])

    #check for pre reqs
    new_class_list = []
    for key,val in p.items():
        for k, v in pre_reqs.items():
            if key == k:
                v = ''.join(v)
                if v in classes.keys():
                    new_class_list.append(key)

    df = preprocess_data()
    #converts user class grades to gpa so that we can compare to the class averages
    grades2gpa = {"A+": 4.00, "A": 4.00, "A-": 3.67, "B+": 3.33, "B": 3.00,
                  "B-": 2.67, "C+": 2.33, "C": 2.00, "C-": 1.67, "D+": 1.33,
                  "D": 1.00, "D-": 0.67, "F": 0.00
                  }

    for key, grade in classes.items():
        if grade in grades2gpa:
            new_grade = grades2gpa[grade]
            classes[key] = grade, new_grade
    #calculates the difference between the user's grade and the grade average for that class
    var = {}
    for k, v in classes.items():
        x_bar = float(df.loc[(df['Class'] == k)]['Average GPA'])
        var[k] = (v[1] - x_bar)

    print(var)
#weights based on gpa performance/ not completely working

    for key in new_class_list:
        top1 = data[key][7][2:-2].split("', '")
        for k,v in pre_reqs.items():
            if key == k:
                top2 = data[value][7][2:-2].split("', '")
                print(top2)
                topic = list(set(top1).intersection(top2))
                if topic != [] and topic != ['N/A']:
                    if var[k] >= 0:
                        weight = 1
                    else:
                        weight = 0.5
                    print(key, weight)






if __name__ == '__main__':
    main()
