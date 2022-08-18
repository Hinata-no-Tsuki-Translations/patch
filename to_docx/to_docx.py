#pip install python-docx

import os
from docx import Document

files = os.listdir('.')

for file in files:

    if file.endswith('.src'):
        print(file)

        with open(file, encoding='shift_jis', mode='r') as f:
            text = f.read()

        document = Document()

        document.add_paragraph(text)

        document.save(file+'.docx')
