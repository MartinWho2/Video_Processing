import csv
LEN_FILES = 67

files = []
for i in range(LEN_FILES):
    with open(str(i)+".txt","r") as f:
        file = f.read()
        files.append(file)
length = []
holding = False
dic = {"0":"1","1":"0"}
for i in range(LEN_FILES):
    file = files[i]
    length.append([])
    reading = "0"
    l = 0
    for char in file:
        if char == reading:
            l += 1
        else:
            length[i].append(l)
            l = 1
            reading = dic[reading]
    length[i].append(l)

ronde = 100
blanche = round(ronde/2)
noire_pointée = round(ronde*3/8)
noire = round(ronde/4)
croche_pointée = round(ronde*3/16)
croche = round(ronde/8)
double_croche = round(ronde/16)
notes = {ronde:"ronde",blanche:"blanche",noire_pointée:"noire_pointee",noire:"noire",croche_pointée:"croche_pointee",
        croche:"croche",double_croche:"double_croche"}
durations = [ronde,blanche,noire_pointée,noire,croche_pointée,croche,double_croche]

def get_duration(note):
    return notes[min(durations, key=lambda x: abs(x - note))]

def write_real_notes(notes):
    final = []
    playing = False
    for note in notes:
        if not playing:
            time = round (note/25 / 0.25) * 0.25
        else:
            time = get_duration(note)
        playing = not playing
        final.append(time)
    return final
for i in range(LEN_FILES):
    with open(str(i)+".csv","w") as file:
        read = csv.writer(file, delimiter=";")
        text = write_real_notes(length[i])
        read.writerow(text)