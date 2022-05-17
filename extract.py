import os
input_folder = 'script'
output_folder = 'output'
files = os.listdir(input_folder)

for file in files:
    tsv_file = ''     # tab separator

    filepath = os.path.join(input_folder, file)
    if os.path.isfile(filepath):
        ext = os.path.splitext(filepath)[-1].lower()
        if ext == ".src":
            with open(filepath, encoding='shift_jis') as f:
                lines = f.readlines()
                for line_no, line in enumerate(lines):
                    if line == '' or line =='\n':
                        pass
                    else:
                        if line[0] == ';' or line[0] == '#':
                            pass
                        else:
                            tsv_file += str(line_no) + "\t" + line
                            
            g = open(os.path.join(output_folder, file + '.tsv'), encoding='utf-8', mode="w")
            g.write(tsv_file)

            
