## Install python-docx
```
pip install python-docx
```

## Translate with Google translate Document upload

1. Convert all src files to docx file by placing in `to_docx` folder and running `to_docx.py`
2. Upload docx files to Google translate one at a time and save translated docx file to `from_docx` folder
3. Run `from_docx.py` to convert all docx file back to src files.
4. Clean src file code commands using `insert-script-commands`  
  4a. Move all src files to `insert-script-commands > old` folder  
  4b. Ensure good code command files in `insert-script-commands > new` folder  
  4c. Run `insert_patch.py`  
  4d. Get src files from `insert-script-commands > out` folder  


Happy machine translating!
