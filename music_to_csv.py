import csv

LEN_FILES = 67

files = []
for i in range(LEN_FILES):
    with open(str(i) + "_new.txt", "r") as f:
        file = f.read()
        files.append(file)
length = []
holding = False
for i in range(LEN_FILES):
    file = files[i]
    length.append([])
    reading = False
    l = 0
    for char in file:
        if not reading:
            reading = char
        if char == reading:
            l += 1
        else:
            length[i].append([reading,l])
            l = 1
            reading = False
    length[i].append([reading,l])

whole = 102
half = round(whole / 2)
dotted_quarter = round(whole * 3 / 8)
quarter = round(whole / 4)
dotted_eighth = round(whole * 3 / 16)
eighth = round(whole / 8)

notes = {whole: "whole", half: "half", dotted_quarter: "dotted_quarter", quarter: "quarter",
         dotted_eighth: "dotted_eighth",
         eighth: "eighth"}
durations = [whole, half, dotted_quarter, quarter, dotted_eighth, eighth]


def get_duration(note):
    return notes[min(durations, key=lambda x: abs(x - note))]

hands = {"1":"-left","2":"-right"}
def write_real_notes(times):
    final = []
    for note in times:
        if note[0] == "0":
            time = round(note[1] / 25 / 0.5) * 0.5
            #time = note[1]/25
        else:
            time = get_duration(note[1]) + hands[note[0]]
        final.append(time)
    return final


for i in range(LEN_FILES):
    with open(str(i) + ".csv", "w") as file:
        read = csv.writer(file, delimiter=";")
        text = write_real_notes(length[i])
        read.writerow(text)
