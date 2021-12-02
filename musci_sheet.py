from xml.dom import minidom
import csv
LEN_FILES = 67
root = minidom.Document()
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

for i in range(LEN_FILES):
    with open(str(i)+".csv","r") as file:
        read = csv.reader(file, delimiter=";")
        for row in read:
            print(row)
            for i in range(1,len(row)+1,2):
                print(get_duration(int(row[i])),end=" ")


xml = root.createElement('score-partwise')
root.appendChild(xml)
xml.setAttribute("version", "4.0")
parts = root.createElement("part-list")
parts = root.appendChild(parts)
p1 = parts.createElement("score-part")
parts.setAttribute("id","P1")
parts.appendChild(p1)

xml.appendChild(parts)

xml_str = root.toprettyxml(indent="\t")

save_path_file = "gfg.xml"

with open(save_path_file, "w") as f:
    f.write(xml_str)