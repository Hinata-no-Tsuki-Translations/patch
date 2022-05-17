import pandas as pd     # need to pip install pandas and openpyxl
import os
import glob

input_folder = 'translated_excel'
output_folder = 'translated_script'   # place scripts to overwrite here

files = os.listdir(input_folder)

for file in files:
    filepath = os.path.join(input_folder, file)
    if os.path.isfile(filepath):
        name = os.path.splitext(file)[0].lower()
        ext = os.path.splitext(filepath)[-1].lower()
        if ext == ".xlsx":
            df = pd.read_excel(filepath, header=None, names=['index', 'original', 'translated'])
            df.fillna('', inplace=True)   # if no translations
            print(df)
            print(os.path.join(output_folder, name))
            filepath2 = glob.glob(os.path.join(output_folder, name))[0]
            print(filepath2)

            new_lines = ''
            with open(filepath2, encoding='shift_jis', mode="r") as f:
                lines = f.readlines()
                for row in df.itertuples():
                    if row.translated == '':
                        print('no translation')
                    elif int(row.index) > len(lines):
                        print('index error')
                    elif lines[int(row.index)] == row.original + "\n":  # replace with sentence similarity?
                        lines[int(row.index)] = row.translated
                        print('translated: line' + str(int(row.index)))
                    elif lines[int(row.index)] == row.translated + "\n":
                        print('translated already')
                    else:
                        print("mismatched: " + lines[int(row.index)] + row.original)

                new_lines = lines
            
            with open(filepath2, encoding='shift_jis', mode="w") as g:
                g.writelines(lines)
