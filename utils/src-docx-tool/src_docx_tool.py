import os
import argparse
import json
from pathlib import Path
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

ENCODING = 'shift_jis'
CONFIG_FILE = 'config.json'

def combine_src_to_docx(output_filename):
    doc = Document()
    for file in Path('.').glob('*.src'):
        doc.add_paragraph(file.name).alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        doc.add_paragraph('-' * 40)

        with file.open('r', encoding=ENCODING, errors='ignore') as f:
            for line in f:
                doc.add_paragraph(line.strip())

        doc.add_page_break()

    doc.save(output_filename)
    print(f"Combined .src files into {output_filename}")

def split_docx_to_src(input_filename):
    # Load config
    if not Path(CONFIG_FILE).exists():
        print(f"Config file '{CONFIG_FILE}' not found.")
        return

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)

    script_folder = Path(config.get('script_folder', '.'))
    if not script_folder.exists():
        print(f"Script folder '{script_folder}' not found.")
        return

    doc = Document(input_filename)
    src_files = {}
    current_filename = None
    content_lines = []

    for para in doc.paragraphs:
        if para.text.endswith('.src') and len(para.text.strip()) > 4:
            if current_filename and content_lines:
                src_files[current_filename] = content_lines
            current_filename = para.text.strip()
            content_lines = []
        elif para.text == '-' * 40 or para.text.strip() == '':
            continue
        else:
            content_lines.append(para.text)

    if current_filename and content_lines:
        src_files[current_filename] = content_lines

    for filename, new_lines in src_files.items():
        original_path = script_folder / filename
        if not original_path.exists():
            print(f"Original script not found: {original_path}")
            continue

        with original_path.open('r', encoding=ENCODING, errors='ignore') as f:
            original_lines = f.readlines()

        replaced_lines = []
        new_line_iter = iter(new_lines)
        for line in original_lines:
            stripped = line.lstrip()
            if stripped.startswith(';') or stripped.startswith('#'):
                try:
                    replacement = next(new_line_iter)
                    replaced_lines.append(replacement + '\n')
                except StopIteration:
                    replaced_lines.append(line)
            else:
                replaced_lines.append(line)

        with open(filename, 'w', encoding=ENCODING, errors='ignore') as f:
            f.writelines(replaced_lines)

        print(f"Created {filename} with replaced lines.")

def main():
    parser = argparse.ArgumentParser(description="Combine or split .src files and .docx documents.")
    subparsers = parser.add_subparsers(dest='command')

    combine_parser = subparsers.add_parser('combine', help='Combine all .src files into a .docx')
    combine_parser.add_argument('output', help='Output .docx filename')

    split_parser = subparsers.add_parser('split', help='Split .docx into .src files with line replacements')
    split_parser.add_argument('input', help='Input .docx filename')

    args = parser.parse_args()

    if args.command == 'combine':
        combine_src_to_docx(args.output)
    elif args.command == 'split':
        split_docx_to_src(args.input)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
