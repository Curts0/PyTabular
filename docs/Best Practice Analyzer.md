#


## BPA
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/best_practice_analyzer.py\#L34)
```python 
BPA(
   File_Path: str = 'Default'
)
```


---
Setting BPA Class for future work...


----


### Download_BPA_File
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/best_practice_analyzer.py\#L8)
```python
.Download_BPA_File(
   Download_Location: str = 'https: //raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json',
   Folder: str = 'Best_Practice_Analyzer', Auto_Remove = True
)
```

---
Runs a request.get() to retrieve the json file from web. Will return and store in directory. Will also register the removal of the new directory and file when exiting program.


**Args**

* **Download_Location** (_type_, optional) : F. Defaults to [Microsoft GitHub BPA]'https://raw.githubusercontent.com/microsoft/Analysis-Services/master/BestPracticeRules/BPARules.json'.
* **Folder** (str, optional) : New Folder String. Defaults to 'Best_Practice_Analyzer'.
* **Auto_Remove** (bool, optional) : If you wish to Auto Remove when script exits. Defaults to True.


**Returns**

* **str**  : File Path for the newly downloaded BPA.

