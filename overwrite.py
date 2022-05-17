import pandas as pd
import glob

input_folder = 'translated_excel'
output_folder = 'translated_script'   # place scripts to overwrite here

files = os.listdir(input_folder)

for file in files:
    filepath1 = os.path.join(input_folder, file)
    if os.path.isfile(filepath):
        name = os.path.splitext(filepath)[0].lower()
        ext = os.path.splitext(filepath)[-1].lower()
        if ext == ".xlsx":
            df = pd.read_excel(filepath1, header=None, names=['index', 'original', 'translated'])
            print(df)
            filepath2 = glob.glob(os.path.join(output_folder, name))
            with open(filepath2, encoding='shift_jis', mode="w") as f:
                lines = f.readlines()
                for row in df.itertuples():
                    if lines[index] == row.original:  # replace with sentence similarity?
                        lines[index] = row.translated
                    else:
                        print("mismatched")
                g.write(lines)
