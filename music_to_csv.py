import csv

LEN_FILES = 67
MESURE = (4,4)
MESURE_DURATION = 103
files = []
for i in range(LEN_FILES):
    with open(str(i) + "_new.txt", "r") as f:
        file = f.read()
        files.append(file)
length = []
holding = False


def get_approx(number, supposed, margin=0.03):
    return abs(supposed - number) < (supposed*margin)


for i in range(LEN_FILES):
    file = files[i]
    length.append([])
    reading = False
    l = 0
    note_time = 1
    measure = []
    for char in file:
        if not reading:
            reading = char
        if char == reading:
            l += 1
        else:
            measure.append([reading, l])
            if get_approx(note_time, MESURE_DURATION):
                note_time = 0
                length[i].append(measure)
                measure = []
            l = 0
            reading = False
        if note_time == MESURE_DURATION:
            measure.append([reading, l])
            note_time = 0
            length[i].append(measure)
            measure = []
            l = 0
        note_time += 1


whole = 103
half = round(whole / 2)
dotted_quarter = round(whole * 3 / 8)
quarter = round(whole / 4)
eighth = round(whole / 8)
#dotted_eighth = round(whole * 3 / 16)
sixteenth = round(whole/16)
notes = {whole: "whole", half: "half", dotted_quarter: "dotted_quarter", quarter: "quarter",
         eighth: "eighth", sixteenth: "sixteenth"}

durations = [whole, half, dotted_quarter, quarter, eighth,sixteenth]

name_to_dur = {"whole": 4, "half": 2, "dotted_quarter": 1.5, "quarter": 1, "eighth": 0.5, "dotted_eighth": 0.75,
               "sixteenth": 0.25}
def get_duration(note):
    return notes[min(durations, key=lambda x: abs(x - note))]


hands = {"1":"-l","2":"-r"}

def write_real_notes(times):
    final = []

    for measure in times:
        mesure = []
        for note in measure:
            if note[0] == "0":
                time = round(note[1] / (103/4) / 0.25) * 0.25
                # time = note[1]/(103/4)
            else:
                time = get_duration(note[1]) + hands[note[0]]
            mesure.append(time)
        sum = 0
        for element in mesure:
            try:
                sum += float(element)
            except:
                sum += name_to_dur[element[:-2]]
        if sum != 4.0:
            if sum < 4:
                if type(mesure[-1]) == float:
                    mesure[-1] += 4-sum
                else:
                    mesure.append(4-sum)
            else:
                if type(mesure[-1]) == float:
                    mesure[-1] -= sum-4
                else:
                    if type(mesure[-2]) == float:
                        mesure[-2] -= sum-4
                    else:
                        print(mesure)
        final.append(mesure)
    return final


for i in range(LEN_FILES):
    with open(str(i) + ".csv", "w") as file:
        read = csv.writer(file, delimiter=";")
        text = write_real_notes(length[i])
        read.writerow(text)
