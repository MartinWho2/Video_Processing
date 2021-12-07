file_name = "music_sheet.txt"
file = open(file_name,"w")
LEN_FILES = 67
for i in range(67):
    with open(str(i)+"_new.txt","r") as f:
        text = f.read()
        file.write(text+"\n")


def get_last_one(string: str) -> int:
    length = len(string)
    for char in range(length):
        a = string[-1]
        if a == "0":
            string = string[:-1]
        else:
            return length - char
    return 0


last_ones = []
for i in range(LEN_FILES):
    file = open(str(i)+".txt","r")
    last_ones.append(get_last_one(file.read()))
    file.close()
end = max(last_ones)

for i in range(LEN_FILES):
    file = open(str(i)+".txt","r")
    text = file.read()
    file.close()
    new_file = open(str(i)+"_new.txt","w")
    new_file.write(text[:end])
