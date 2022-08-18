## Steps to translate with Google translate Document upload

1. Convert all src files to docx file by placing in `to_docx` folder and running `to_docx.py`
2. Upload docx files to Google translate one at a time and save translated docx file to `from_docx` folder
3. Run `from_docx.py` to convert all docx file back to src files.
4. Clean src file code commands using `patch_update`  
  4a. Move all src files to `patch_update > old` folder  
  4b. Ensure good code command files in `patch_update > new` folder  
  4c. Run `insert_patch.py`  
  4d. Get src files from `patch_update > out` folder  


Happy machine translating!
