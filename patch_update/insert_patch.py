import os
import glob

old_folder = 'old'      # old scripts with english translations
new_folder = 'new'      # new scripts with japanese
out_folder = 'out'

def is_text(line):
    return line and line != '' and line !='\n' and not line.isspace() and line[0] != ';' and line[0] != '#'

files = os.listdir(old_folder)

for file in files:
    print(file)
    
    old_file = os.path.join(old_folder, file)

    if not os.path.isfile(old_file):
        continue
    
    try:
        new_file = glob.glob(os.path.join(new_folder, file))[0]
    except IndexError:
        continue
    
    out_file = os.path.join(out_folder, file)

    ext = os.path.splitext(file)[-1].lower()

    if ext != ".src":
        continue
    
    with open(new_file, encoding='shift_jis', mode='r') as f:
        new_lines = f.readlines()
    with open(old_file, encoding='shift_jis', mode='r') as g:
        old_lines = g.readlines()

    nn = 0
    for oo, o in enumerate(old_lines):
        if is_text(o):
            while nn < len(new_lines):
                if is_text(new_lines[nn]):
                    print('Replace ' + new_lines[nn] + ' with ' + o)
                    new_lines[nn]=o
                    break
                nn+=1
            nn+=1

    with open(out_file, encoding='shift_jis', mode="w") as h:
        h.writelines(new_lines)
