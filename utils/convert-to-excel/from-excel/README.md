## Install pandas and openpyxl

```
pip install pandas
```

```
pip install openpyxl
```


## Insert excel xlsx translations to src file

1. excel xlsx file with translated Eng column in `excel` folder
2. original src file in `script` folder
3. Run `insert.py`
4. output src file in `out` folder


### Note:
- Does not check Jpn text with original text before replacing
- Uses Line column in excel file to find text to replace
- Uses Edit column over Eng column if Edit column is not empty
