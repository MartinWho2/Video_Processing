from xml.dom import minidom
import csv
LEN_FILES = 67

files = []
for i in range(LEN_FILES):
    file = open(str(i)+".csv","r")
    reader = csv.reader(file,delimiter=";")
    measures = []
    for row in reader:
        measures.append(row)
    files.append(measures)
print(files)