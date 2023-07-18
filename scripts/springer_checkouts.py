# Script to visualize checkouts of Springer titles in various categories by Stephen Hall



# Delete header rows
# Make sure total usage column is in "General" format (with no commas)

import csv
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider

def read_and_clean(filename):

    rows = []

    # Read CSV and create list of lists
    with open(filename, 'r') as csvfile:

        plots = csv.reader(csvfile, delimiter = ',')
        for row in plots:

            # itemgetter grabs items at specified indexes, ignoring others
            x = itemgetter(0,1,2,12)(row)
            rows.append(x)

    # Remove header info
    #i = [i for i, x in enumerate(rows) if "Title" in x]
    #del rows[0:(i[0] - 1)]
    return(rows)

sheet1 = read_and_clean('/users/smhall/Desktop/Library Operations/Springer Usage/U Penn 2020-2021 MyCollection Usage Stats_June 2020 to April 2021.csv')
sheet2 = read_and_clean('/users/smhall/Desktop/Library Operations/Springer Usage/U Penn 2021-2022 MyCollection Usage Stats_June 2021 to May 2022.csv')
sheet3 = read_and_clean('/users/smhall/Desktop/Library Operations/Springer Usage/U Penn 2022-2023 MyCollection Usage Stats_June 2022 to May 2023.csv')


isbn1 = [i[1] for i in sheet1]
isbn2 = [i[1] for i in sheet2]
isbn3 = [i[1] for i in sheet3]

unique = list(set(isbn1+isbn2+isbn3))


out = "/users/smhall/Desktop//Library Operations/Springer Usage/Multiyear Use (20-23).csv"
    
# writing to csv file 
with open(out, 'w') as output: 
    csvwriter = csv.writer(output)

    csvwriter.writerow(['BOOKS CHECKED OUT IN 20-21 AND 21-22'])
    csvwriter.writerow(['Title', 'ISBN', 'Collection', '2020-2021 Usage', '2021-2022 Usage'])
    
    for i in sheet1:
        for j in sheet2:
            if i[1] == j[1] and int(i[3]) > 0 and int(j[3]) > 0:
                csvwriter.writerow([i[0], i[1], i[2], i[3], j[3]])
                
    csvwriter.writerow([''])
    csvwriter.writerow([''])

    csvwriter.writerow(['BOOKS CHECKED OUT IN 21-22 AND 22-23'])
    csvwriter.writerow(['Title', 'ISBN', 'Collection', '2021-2022 Usage', '2022-2023 Usage'])

    for i in sheet2:
        for j in sheet3:
            if i[1] == j[1] and int(i[3]) > 0 and int(j[3]) > 0:
                csvwriter.writerow([i[0], i[1], i[2], i[3], j[3]])


    csvwriter.writerow([''])
    csvwriter.writerow([''])

    csvwriter.writerow(['BOOKS CHECKED OUT IN 21-22, 22-23, AND 22-23'])
    csvwriter.writerow(['Title', 'ISBN', 'Collection', '2020-2021 Usage', '2021-2022 Usage', '2022-2023 Usage'])

    for i in sheet1:
        for j in sheet2:
            for k in sheet3:
                if i[1] == j[1] and j[1] == k[1] and int(i[3]) > 0 and int(j[3]) > 0 and int(k[3]) > 0:
                    csvwriter.writerow([i[0], i[1], i[2], i[3], j[3], k[3]])


