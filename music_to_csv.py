import csv
import math
from xml.dom import minidom
import xml.etree.ElementTree as ET
LEN_FILES = 67
MESURE = (4, 4)
MESURE_DURATION = 103
files = []
for i in range(LEN_FILES):
    with open(str(i) + "_new.txt", "r") as f:
        file = f.read()
        files.append(file)
length = []
holding = False


def get_approx(number, supposed, margin=0.03):
    return abs(supposed - number) < (supposed * margin)


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

whole = MESURE_DURATION
half = round(whole / 2)
dotted_half = round(whole*3/4)
dotted_quarter = round(whole * 3 / 8)
quarter = round(whole / 4)
eighth = round(whole / 8)
dotted_eighth = round(whole * 3 / 16)
sixteenth = round(whole / 16)
notes = {whole: "whole",dotted_half:"dotted_half", half: "half", dotted_quarter: "dotted_quarter", quarter: "quarter",
         eighth: "eighth",dotted_eighth:"dotted_eighth",sixteenth:"sixteenth"}

durations = [whole, dotted_half, half, dotted_quarter, quarter, dotted_eighth, eighth, sixteenth]

name_to_dur = {"whole": 4,"dotted_half": 3, "half": 2, "dotted_quarter": 1.5, "quarter": 1, "eighth": 0.5, "dotted_eighth": 0.75,
               "sixteenth": 0.25}

def get_silence(silence:int):
    difference = []
    names = []
    for silences in name_to_dur.items():
        dif = silence-silences[1]
        if dif > 0:
            difference.append(dif)
            names.append(silences[0])
        if dif in {0, 0.0}:
            return silences[0]
    print(difference, silence)
    indexing = difference.index(min(difference))
    first_note = names[indexing]
    lasting = difference[indexing]
    for silences in name_to_dur.items():
        dif = lasting - silences[1]
        if dif in {0, 0.0}:
            second_note = silences[0]
    return [first_note, second_note]


def get_duration(note_length):
    print(min(durations, key=lambda x: abs(x - note_length)))
    return notes[min(durations, key=lambda x: abs(x - note_length))]

hands = {"1": "l", "2": "r"}


def write_real_notes(times):
    final = []

    for measure in times:
        mesure = []
        for note in measure:
            if note[0] == "0":
                time = round(note[1] / (whole / 4) / 0.25) * 0.25
                # time = note[1]/(103/4)
            else:
                time = hands[note[0]] + get_duration(note[1])
            mesure.append(time)
        sum = 0
        for element in mesure:
            try:
                sum += float(element)
            except:
                sum += name_to_dur[element[1:]]
        if sum != 4.0:
            if sum < 4:
                if type(mesure[-1]) == float:
                    mesure[-1] += 4 - sum
                else:
                    mesure.append(4 - sum)
            else:
                if type(mesure[-1]) == float:
                    if mesure[-1] >= sum-4:
                        mesure[-1] -= sum - 4
                else:
                    if type(mesure[-2]) == float:
                        if mesure[-2] >= sum - 4:
                            mesure[-2] -= sum - 4
                    else:
                        if type(mesure[-3]) == float:
                            if mesure[-3] >= sum - 4:
                                mesure[-3] -= sum - 4
                        else:
                            if type(mesure[-4]) == float:
                                if mesure[-4] >= sum - 4:
                                    mesure[-4] -= sum - 4
                            else:
                                if type(mesure[-5]) == float:
                                    if mesure[-5] >= sum - 4:
                                        mesure[-5] -= sum - 4
        final.append(mesure)
    return final


n_measure = []
med_music = []
for i in range(len(length)):
    # with open(str(i) + ".csv", "w") as file:
    # read = csv.writer(file, delimiter=";")
    # text = write_real_notes(length[i])
    # read.writerow(text)
    n_measure.append(len(length[i]))
    med_music.append(write_real_notes(length[i]))

def get_silence_before(mesure:list, index:int):
    silence = 0
    for i in range(len(mesure)):
        if i == index:
            break
        else:
            time = mesure[i]
            if type(mesure[i]) == str:
                time = name_to_dur[mesure[i][1:]]
            silence += time
    return silence


def get_chords(mesure: dict):
    new_mesure = [note for note in mesure.items()]
    #print(new_mesure)
    complete_mesure = {"r": [], "l": []}
    for key in new_mesure:
        tone = key[0]
        for j in range(len(key[1])):
            note = key[1][j]

            if type(note) == str:
                complete_mesure[note[0]].append([tone, get_silence_before(key[1],j), note[1:]])
    #print(complete_mesure)
    first_notes = []
    for note in new_mesure:
        if type(note[1][0]) != float:
            first_notes.append(note[0])
    #print(first_notes)
    # for division in range(16):
    #print(order_mesure(complete_mesure["r"]))

def order_mesure(mesure:list):
    mesure_copy = mesure[:]
    pauses = [note[1] for note in mesure]
    pauses = sorted(pauses)
    sorted_mesure = []
    for _ in range(len(mesure_copy)):
        mesure_to_del = []
        chord_list = []
        for note in mesure_copy:
            if note[1] == pauses[0]:
                chord_list.append(note)
                mesure_to_del.append(note)
        for element in mesure_to_del:
            del mesure_copy[mesure_copy.index(element)]
        del pauses[0]
        if chord_list:
            sorted_mesure.append(chord_list)
    return sorted_mesure

def get_note_from_index(index:int):
    letters = {0:"C",1:"C",2:"D",3:"D",4:"E",5:"F",6:"F",7:"G",8:"G",9:"A",10:"A",11:"B"}
    flats = {0:0,1:1,2:0,3:1,4:0,5:0,6:1,7:0,8:1,9:0,10:1,11:0}
    note = letters[index % 12]
    height = math.floor(index/12)+1
    flat = flats[index % 12]
    return [note, height, flat]
def create_binary_map(mesure: list):
    binary_map = []
    for element in mesure:
        if type(element) == float:
            while element != 0.0:
                binary_map.append(0)
                element -= 0.25
        elif type(element) == str:
            hand = element[-1]


final_music = []
for measure in range(len(med_music[0])):
    a = {}
    for note in range(len(med_music)):
        mesure = med_music[note][measure]
        if mesure[0] != 4.0:
            a[note] = mesure
    final_music.append(a)
print(final_music)

for measure in final_music:
    hands_parts = {"r":[],"l":[]}
    for key in measure.items():
        key_number = key[0]
        for note in key[1]:
            if type(note)== str:
                hands_parts[note[0]].append([key_number,note])
# This whole method sucks but I have no idea how to make it any better
# I need to get from a measure that has keys identified separately (as if it was a voice) to a measure where they are all combined IRT




print(write_real_notes(length[0]))
measures = []
for key in length:
    measures.append(write_real_notes(key))

partition = ET.Element("score-partwise")
partition.set("version", "3.1")
part_list = ET.SubElement(partition, "part-list")
for i in range(LEN_FILES):
    part_id = str(i)
    key_from_id = get_note_from_index(i)
    part_in_list = ET.SubElement(part_list, "score-part")
    part_in_list.set("id", part_id)
    part_name = ET.SubElement(part_in_list, "part-name")
    part_name.text = part_id
    part = ET.SubElement(partition, "part")
    part.set("id", part_id)
    data = measures[i]
    for integer in range(len(data)):
        xml_measure = ET.SubElement(part,"measure")
        xml_measure.set("number", str(integer+1))
        if integer == 0:
            attibrute = ET.SubElement(xml_measure,"attributes")
            divisions = ET.SubElement(attibrute,"divisions")
            divisions.text = "4"
            key = ET.SubElement(attibrute,"key")
            fifths = ET.SubElement(key,"fifths")
            fifths.text = "0"
            time = ET.SubElement(attibrute,"time")
            beats = ET.SubElement(time,"beats")
            beats.text = "4"
            beat_type = ET.SubElement(time, "beat-type")
            beat_type.text = "4"
            stave = ET.SubElement(attibrute,"staves")
            stave.text = "1"
            clef = ET.SubElement(attibrute,"clef")
            clef.set("number","1")
            clef_f_or_g = ["G","2"]
            if integer < 48 :
                clef_f_or_g = ["F","4"]
            sign = ET.SubElement(clef,"sign")
            sign.text = clef_f_or_g[0]
            line = ET.SubElement(clef, "line")
            line.text = clef_f_or_g[1]
        for element in data[integer]:
            print(element, integer)
            if integer == 27:
                print(data[27])
            if element not in {0,0.0}:

                if type(element) == str:
                    note = ET.SubElement(xml_measure,"note")
                    pitch = ET.SubElement(note,"pitch")
                    step = ET.SubElement(pitch,"step")
                    step.text = key_from_id[0]
                    octave = ET.SubElement(pitch, "octave")
                    octave.text = str(key_from_id[1])
                    if key_from_id != 0:
                        alter = ET.SubElement(pitch,"alter")
                        alter.text = str(key_from_id[2])
                    duration = ET.SubElement(note, "duration")
                    voice = ET.SubElement(note, "voice")
                    voice.text = "1"
                    type_note = ET.SubElement(note, "type")
                    if element[1:8] == "dotted_":
                        duration.text = str(int(name_to_dur[element[8:]] * 6))
                        type_note.text = str(element[8:])
                        dot = ET.SubElement(note,"dot")
                    else:
                        duration.text = str(int(name_to_dur[element[1:]] * 4))
                        type_note.text = element[1:]
                else:
                    note = ET.SubElement(xml_measure, "note")
                    rest = ET.SubElement(note, "rest")
                    duration = ET.SubElement(note, "duration")
                    voice = ET.SubElement(note, "voice")
                    voice.text = "1"
                    type_note = ET.SubElement(note,"type")
                    silence = get_silence(element)
                    if type(silence) == str:
                        if silence[:7] == "dotted_":
                            duration.text = str(int(name_to_dur[silence] * 4))
                            type_note.text = str(silence[7:])
                            dot = ET.SubElement(note,"dot")
                        else:
                            duration.text = str(int(name_to_dur[silence] * 4))
                            type_note.text = silence
                    elif type(silence) == list:
                        note_1 = silence[0]
                        if note_1[:7] == "dotted_":
                            duration.text = str(int(name_to_dur[note_1] * 4))
                            type_note.text = str(note_1[7:])
                            dot = ET.SubElement(note,"dot")
                        else:
                            duration.text = str(int(name_to_dur[note_1] * 4))
                            type_note.text = note_1
                        note = ET.SubElement(xml_measure, "note")
                        rest = ET.SubElement(note, "rest")
                        duration = ET.SubElement(note, "duration")
                        voice = ET.SubElement(note, "voice")
                        voice.text = "1"
                        type_note = ET.SubElement(note, "type")
                        if silence[1][:7] == "dotted_":
                            duration.text = str(int(name_to_dur[silence[1]] * 4))
                            type_note.text = silence[1][7:]
                            dot = ET.SubElement(note,"dot")
                        else:
                            duration.text = str(int(name_to_dur[silence[1]] * 4))
                            type_note.text = silence[1]

mydata = ET.tostring(partition)
myfile = open("partition.xml", "wb")
myfile.write(mydata)


