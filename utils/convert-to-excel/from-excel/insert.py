import pandas as pd     # need to pip install pandas and openpyxl
import os
import glob

excel_folder = 'excel'      # needs to have Line, Jpn, Eng, Edit columns
script_folder = 'script'
out_folder = 'out'

files = os.listdir(excel_folder)

for file in files:
    excel_file = os.path.join(excel_folder, file)

    if not os.path.isfile(excel_file):
        continue
    
    name = os.path.splitext(file)[0].lower()   # jyo01.src without xlsx extension
    try:
        script_file = glob.glob(os.path.join(script_folder, name))[0]
    except IndexError:
        continue
    
    out_file = os.path.join(out_folder, name)

    ext = os.path.splitext(file)[-1].lower()

    if ext != ".xlsx":
        continue

    df = pd.read_excel(excel_file, header=0, usecols=['Line', 'Jpn', 'Eng', 'Edit'])
    df.fillna('', inplace=True)   # if no translations

    with open(script_file, encoding='shift_jis', mode='r') as f:
        lines = f.readlines()
    
    added_num = 0
    for row in df.itertuples():

        if not row.Line or str(row.Line) == '':
            continue

        ln = "Line " + str(row.Line) + ': '

        if not row.Eng or row.Eng == '' or row.Eng == "\n" or row.Eng.isspace() :
            print(ln + 'no translation')

        elif row.Eng[0] == ';' or row.Eng[0] == '#' or (row.Edit and len(row.Edit) > 0 and (row.Edit[0] == ';' or row.Edit[0] == '#')):
            print(ln + 'translation cannot have script calls')
            
        elif row.Line > len(lines) or row.Line < 0:
            print(ln + 'index error')

        line = lines[row.Line]

        if not line or line == '' or line == "\n" or line.isspace() or line[0] == ';' or line[0] == '#':
            print(ln + 'empty line in script')

        elif line != row.Jpn + "\n" and line != row.Eng + "\n" and line != row.Edit + "\n":
            print(ln + 'misaligned - \n\t' + line[0:5] + '\t|\t' + row.Jpn[0:5])

        elif row.Edit and row.Edit != '':
            lines[row.Line] = row.Edit + "\n"
            added_num += 1
            print(ln + 'edited - \t' + row.Edit[0:10])

        elif row.Eng and row.Eng != '':
            lines[row.Line] = row.Eng + "\n"
            added_num += 1
            #print(ln + 'added - \t' + row.Eng[0:10])

        else:
            print(ln + 'unknown case ERROR')
    
    with open(out_file, encoding='shift_jis', mode="w") as g:
        g.writelines(lines)
        
    print(file + '\tTranslated: ' + str(added_num) + '/' + str(len(df)))
