import os
import glob

jpn_folder = "jpn"
counts = []

files = os.listdir(jpn_folder)

for file in files:
    count = 0

    jpn_file = os.path.join(jpn_folder, file)
    
    if not os.path.isfile(jpn_file):
        continue
    
    ext = os.path.splitext(file)[-1].lower()

    if ext != ".src":
        continue
    
    with open(jpn_file, encoding='shift_jis') as f:
        jpn_lines = f.readlines()
    
    for line in jpn_lines:
        if not line or line == '' or line =='\n' or line.isspace() or line[0] == ';' or line[0] == '#':
            pass
        else:
            count += 1

    print(str(file) + '\t' + str(count))

    counts.append(str(count))

with open('count.txt', 'w') as g:
    g.write('\n'.join(counts))
