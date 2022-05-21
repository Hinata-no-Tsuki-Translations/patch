import pandas as pd
import os
import xlsxwriter       # need to pip install xlsxwriter
import glob

jpn_folder = "jpn"
eng_folder = "eng"
out_folder = 'out'

files = os.listdir(jpn_folder)

for file in files:
    print(file)
    d = {'Line': [], 'Jpn':[], 'Eng':[], 'Edit':[]}

    jpn_file = os.path.join(jpn_folder, file)
    try:
        eng_file = glob.glob(os.path.join(eng_folder, file))[0]
    except IndexError:
        eng_file = None
    out_file = os.path.join(out_folder, file + '.xlsx')

    if not os.path.isfile(jpn_file):
        continue
    
    ext = os.path.splitext(file)[-1].lower()

    if ext != ".src":
        continue
    
    with open(jpn_file, encoding='shift_jis') as f:
        jpn_lines = f.readlines()
    eng_lines = None
    if eng_file is not None:
        with open(eng_file, encoding='shift_jis') as g:
            eng_lines = g.readlines()
        if len(eng_lines) != len(jpn_lines):
            print("Unequal number of lines for japan and english for " + file + ". Engilsh not parsed.")

    for line_no, line in enumerate(jpn_lines):
        if not line or line == '' or line =='\n' or line.isspace() or line[0] == ';' or line[0] == '#':
            pass
        else:
            d['Line'].append(line_no)
            d['Jpn'].append(line.strip())
            if eng_lines:
                d['Eng'].append(eng_lines[line_no].strip())
            else:
                d['Eng'].append('')  # machine translate
                pass
            d['Edit'].append('')

    df = pd.DataFrame(d)
    df.set_index('Line', inplace=True)
    writer = pd.ExcelWriter(out_file, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=file)
    writer.save()