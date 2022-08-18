#pip install python-docx

import os
from docx import Document

files = os.listdir('.')

for file in files:

    if file.endswith('.docx'):
        print(file)

        document = Document(file)

        lines = []
        
        for para in document.paragraphs:
            lines.append(para.text)
        
        fulltext = '\n'.join(lines) + '\n'      # google translate removed line break at end, so add back

        new_file = file[:-5]
        with open(new_file, encoding='shift_jis', mode='w') as f:
            f.write(fulltext)
