#


## Tabular_Editor
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_editor.py\#L38)
```python 
Tabular_Editor(
   EXE_File_Path: str = 'Default'
)
```


---
Setting Tabular_Editor Class for future work.


----


### Download_Tabular_Editor
[source](https://github.com/Curts0/PyTabular\blob\master\pytabular/tabular_editor.py\#L8)
```python
.Download_Tabular_Editor(
   Download_Location: str = 'https: //github.com/TabularEditor/TabularEditor/releases/download/2.16.7/TabularEditor.Portable.zip',
   Folder: str = 'Tabular_Editor_2', Auto_Remove = True
)
```

---
Runs a request.get() to retrieve the zip file from web. Will unzip response and store in directory. Will also register the removal of the new directory and files when exiting program.


**Args**

* **Download_Location** (str, optional) : File path for zip of Tabular Editor 2. Defaults to [Tabular Editor 2 Github Zip Location]'https://github.com/TabularEditor/TabularEditor/releases/download/2.16.7/TabularEditor.Portable.zip'.
* **Folder** (str, optional) : New Folder Location. Defaults to 'Tabular_Editor_2'.
* **Auto_Remove** (bool, optional) : Boolean to determine auto removal of files once script exits. Defaults to True.


**Returns**

* **str**  : _description_

