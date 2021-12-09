from xml.dom import minidom
import csv
LEN_FILES = 67

files = []
n_measure = []
def get_chords(mesure: dict):
    notes = [note[1] for note in mesure.items()]
    print(notes)


for i in range(LEN_FILES):
    file = open(str(i)+".csv", "r")
    reader = csv.reader(file, delimiter=";")
    m = []
    for row in reader:
        m.append(row)
    m = m[0]
    files.append(m)
    n_measure.append(len(m))
final_music = []
for measure in range(len(files[0])):
    a = {}
    for note in range(len(files)):
        mesure = files[note][measure]
        if mesure != "[4.0]":
            a[note] = mesure
    final_music.append(a)
print(final_music)
print(get_chords(final_music[0]))


