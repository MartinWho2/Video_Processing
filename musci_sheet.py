from xml.dom import minidom
import csv
LEN_FILES = 67
root = minidom.Document()

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