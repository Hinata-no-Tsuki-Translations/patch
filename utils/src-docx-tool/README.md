# SRC-DOCX Converter

A Python CLI tool to convert `.src` script files to a formatted `.docx` document ? and back ? while preserving comments and Japanese Shift_JIS encoding.

---

## ? Features

- ? Combine multiple `.src` text files into a single `.docx` with page breaks and filename headings.
- ? Split the `.docx` back into individual `.src` files.
- ? Restores original comment lines (starting with `;` or `#`) from the original `.src` files.
- ? Handles Japanese Shift_JIS encoding.
- ? Uses a configuration file to locate original script files.

---

## ??? Requirements

- Python 3.7+
- `python-docx`

Install dependencies:

```bash
pip install python-docx

pip install -U pip setuptools wheel # prereq for spacy

pip install spacy  # ensure python 3.12 or below as of 2025-Apr or use pip3.12 install
```

---

## ?? Configuration

Create a `config.json` file in the same directory as your script:

```json
{
  "script_folder": "path/to/original/src/files"
}
```

This tells the tool where to find the **original** `.src` files (used during the split to recover comment lines).

---

## ? Usage

```bash
python src_docx_tool.py combine output.docx
python src_docx_tool.py split output.docx
```

### 1. Combine `.src` Files Å® `output.docx`

- Looks for all `.src` files in the **current directory**.
- Combines them into a single `.docx` file.
- Each file:
  - Starts with its filename
  - Has a separator (`----------------------------------------`)  
  - Note: Originally to add a line break here, but removed because it creates an extra line.

### 2. Split `output.docx` Å® `.src` Files

- Splits the `.docx` back into `.src` files using the filename markers.
- Looks up original `.src` files from `script_folder` in `config.json`.
- Replaces lines in the `.docx` output **with original comment lines** (`;` or `#`) from those files.
- Preserves original line breaks and encoding.

---

## ? Notes

- Shift_JIS encoding is used when reading/writing `.src` files.
- Blank lines are preserved during round-trip conversion.
- Does **not** overwrite original `.src` files ? it only writes to current directory.

---

## ? Example Workflow

```bash
# 1. Copy files from script folder into current directory

# 2. Combine all .src files in the current folder into one Word document
python src_docx_tool.py combine output.docx

# 3. Drag drop the output.docx file into Google Translate

# 4. Download the translated .docx file and overwrite the output.docx file

# 5. Split it back into separate .src files and restore original comments
python src_docx_tool.py split output.docx
```

---

## ?? File Structure

```
.
Ñ•ÑüÑü src_docx_tool.py       # The main script
Ñ•ÑüÑü config.json            # Points to japanese .src files
Ñ•ÑüÑü script1.src
Ñ•ÑüÑü script2.src
Ñ§ÑüÑü output.docx     # Output from combine / input for split
```

---
