## Install pandas and xlsxwriter
```
pip install pandas
```

```
pip install xlsxwriter
```

## Extract non-code lines from src file to Excel xlsx file

1. translated src files to `jpn` folder
2. original src files to `eng` folder
3. Run `extract.py`
4. excel output in `out` folder

Example output:  
`b01.src.xlsx`

| Line        | Jpn           | Eng  | Edit |
| ------------- |-------------| -----|---|
| 45    |「……ま、こんなもんか」 |「...Well, that should do it.」  ||


## Count lines of script files in `jpn` folder

1. src files in `jpn` folder
2. Prints list of counts of script files in alphabetical order in `count.txt`
