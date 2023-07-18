# Script to calculate and visualize hourly patron traffic by Stephen Hall

#To run this file, download the latest version of the
# "FY23 Biotech Commons Hourly Patron Count" document.
# The document must be in CSV format, saved in the folder
# where the program reads from.

from __future__ import division
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import csv

rows = []
days = []
y = []

with open('/users/smhall/Desktop/BTC Traffic/FY23 Biotech Commons Hourly Patron Count.csv', 'r') as csvfile:

    plots = csv.reader(csvfile, delimiter = ',')
    for row in plots:
        
        rows.append(row)

del(rows[0])

for row in rows:
    for i in range(3, len(row)):
        if row[i] == '':
            row[i] = 0
        else:
            try:
                row[i] = int(row[i])
            except ValueError:
                pass
for i in rows:
    if i[1] == '':
        pass
    else:
        days.append(i[0:3])
        y.append(i)

days_key = days.pop(0)
x = y.pop(0)[3:]
fig = plt.figure(figsize=(15,10))

sundays = []
mondays = []
tuesdays = []
wednesdays = []
thursdays = []
fridays = []
saturdays = []

for i,j in enumerate(y[0:len(y)]):
    if i % 7 == 5:
        sundays.append(j)
    elif i % 7 == 6:
        mondays.append(j)
    elif i % 7 == 0:
        tuesdays.append(j)
    elif i % 7 == 1:
        wednesdays.append(j)
    elif i % 7 == 2:
        thursdays.append(j)
    elif i % 7 == 3:
        fridays.append(j)
    elif i % 7 == 4:
        saturdays.append(j)

days_lol = [sundays, mondays, tuesdays, wednesdays, thursdays, fridays, saturdays]
day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]


def visualize(day,n):
    
    colors = {
        "1/" : "#7b8eb5",
        "2/" : "#38496b",
        "3/" : "#ffb4d7",
        "4/" : "#ff72a4",
        "5/" : "#ff3f83",
        "6/" : "#93d492",
        "7/" : "#8dc001",
        "8/" : "#5c9e1e",
        "9/" : "#ffb52e",
        "10" : "#ffa500",
        "11" : "#d18700",
        "12" : "#a2baeb"
        }
    
    z = 0
    for i in day:
        j = i[3:]
        if j != [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]:
            z += 1
            c = i[2][0:2] #scatter point color
            if i[0] != '':
                plt.scatter(x, j, marker="+", s=60, color=colors[c], linewidths=2)
            else:
                plt.scatter(x, j, marker="o", s=20, color=colors[c])
    def curve(a):
        if all([isinstance(item, int) for item in a]):
            return sum(a) / z

    curve_mean = [*map(curve, zip(*day))][3:]
    plt.plot(curve_mean, color = '#666666', linestyle = '--', linewidth = 2)

for i in range(len(days_lol)):
    plt.subplot(2,4,i+1)
    visualize(days_lol[i],i+1)
    plt.title(day_names[i])
    plt.xticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], x, rotation=90)

l = [
    Line2D([0],[0],marker="o",color="#7b8eb5",label="January",linestyle="None"),
    Line2D([0],[0],marker="o",color="#38496b",label="February",linestyle="None"),
    Line2D([0],[0],marker="o",color="#ffb4d7",label="March",linestyle="None"),
    Line2D([0],[0],marker="o",color="#ff72a4",label="April",linestyle="None"),
    Line2D([0],[0],marker="o",color="#ff3f83",label="May",linestyle="None"),
    Line2D([0],[0],marker="o",color="#93d492",label="June",linestyle="None"),
    Line2D([0],[0],marker="o",color="#8dc001",label="July",linestyle="None"),
    Line2D([0],[0],marker="o",color="#5c9e1e",label="August",linestyle="None"),
    Line2D([0],[0],marker="o",color="#ffb52e",label="September",linestyle="None"),
    Line2D([0],[0],marker="o",color="#ffa500",label="October",linestyle="None"),
    Line2D([0],[0],marker="o",color="#d18700",label="November",linestyle="None"),
    Line2D([0],[0],marker="o",color="#a2baeb",label="December",linestyle="None"),
    Line2D([0],[0],marker="+",color="black",label="Special Event",linestyle="None"),
    Line2D([0],[0],color="#666666",label="Average",linestyle="--")    
    ]

fig.legend(handles=l,loc='lower right', borderaxespad=8)

fig.tight_layout()
plt.show()
