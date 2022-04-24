from tokenize import String
import zipfile
import json
import os
import pandas as pd
from tkinter import filedialog, Tk, ttk, StringVar, Label



class pbix:
    def __init__(self,file_location=None) -> None:
        def try_recursive(location, initial_try):
            try:
                return location[initial_try]
            except:
                return None

        #Get top level .pbix file items
        if file_location is None:
            file_location = retrieve_pbix_file()
        else:
            pass
        self.zipping = zipfile.ZipFile(file_location)
        self.file_location = file_location
        self.base_file_name = os.path.splitext(os.path.basename(self.file_location))[0]
        self.name_list = self.zipping.namelist()

        #Base Layout Items
        self.layout = json.loads(self.zipping.open('Report/Layout','r').read().decode('utf-16'))
        self.layout_id = self.layout['id']
        self.layout_report_id = try_recursive(self.layout,'reportId')
        self.layout_theme = self.layout['theme']
        self.layout_resource_packages = self.layout['resourcePackages']
        self.layout_sections = self.layout['sections']
        self.layout_optimization = self.layout['layoutOptimization']
        self.layout_publicCustomVisuals = self.layout['publicCustomVisuals']
        self.layout_pods = try_recursive(self.layout,'pods')
        self.layout_config = json.loads(self.layout['config'])

        #Report Level Filters
        self.layout_filters = pd.DataFrame(json.loads(self.layout['filters']))
        
        #Report Level Measures
        report_level_a = pd.DataFrame(self.layout_config['modelExtensions'][0]['entities']).explode('measures').rename(columns={'name':'table'})
        report_level_b = pd.concat([report_level_a, report_level_a['measures'].apply(pd.Series)],axis=1)
        self.report_level_measures = report_level_b.drop(columns=['extends','measures'])

        #Report Pages
        self.report_tabs = pd.DataFrame(self.layout_sections,columns=self.layout_sections_keys)
        page_level_filters_a = self.report_tabs[['id','filters']]
        self.page_level_filters = 1

        #Stats
        self.number_of_report_tabs = len(self.report_tabs)
        self.number_of_report_level_measures = len(self.report_level_measures)
        self.number_of_report_level_filters = len(self.layout_filters)

        pass
    def __repr__(self) -> str:
        return 'PBIX called... raise the roof'

    #Garbage Functions to Remove or Fix
    def get_read_items(self) -> dict():
        layout_dict = open('Report/Layout','r',encoding='utf-16').read()
        return layout_dict

def retrieve_pbix_file():
    root = Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()
    file_location = filedialog.askopenfilename(title='Select a PBIX File', filetypes=[('Microsoft.MicrosoftPowerBIDesktop','*.pbix')], parent = root)
    root.quit
    print(f'Got the file location...{file_location}')
    return file_location


def unzip_all(file_location=None,save_location=None):
    if file_location is None:
        print('What file to unzip?...')
        file_location = retrieve_pbix_file()
    if save_location is None:
        root = Tk()
        root.wm_attributes('-topmost', 1)
        root.withdraw()
        save_location_directory = filedialog.askdirectory(title='Where do you want to save the files?',parent = root)
        save_location = f'{save_location_directory}/{os.path.splitext(os.path.basename(file_location))[0]}'
        root.quit
    with zipfile.ZipFile(file_location) as pbix:
        pbix.extractall(path=save_location)
        pbix.close()
        os.startfile(save_location)
        print(f'Saved Files to {save_location}')

def main_csv_saver(file_name,file_contents,file_location=None,open_file=True):
    if file_location is None or file_name is None:
        root = Tk()
        root.wm_attributes('-topmost', 1)
        root.withdraw()
        file_location = filedialog.asksaveasfilename(
            title='Save As',
            initialfile = file_name,
            defaultextension = [('CSV files',"*.csv")],
            filetypes=[('CSV files',"*.csv")],
            parent = root)
        file_name = os.path.basename(file_location)
        root.quit
    file_contents.to_csv(file_location)
    if open_file:
        os.startfile(file_location)
    return file_contents

def pbix_utility_window():
    pbix_class = pbix()
    def change_file():
        root.destroy()
        pbix_utility_window()

    print('Launching Window...')
    root = Tk()
    tkinter_var_file_location = StringVar(root,pbix_class.file_location)
    tkinter_var_file_name = StringVar(root,pbix_class.base_file_name)
    tkinter_main_label_var = StringVar(root,f'Do stuff with your PBI File - {pbix_class.file_location}')

    root.title(pbix_class.base_file_name)
    root.wm_attributes('-topmost', 1)
    frm = ttk.Frame(root, padding=200)
    frm.grid()
    main_label = Label(frm,textvariable=tkinter_main_label_var).grid(column=0, row=1)

    ttk.Button(frm,text="Change Working PBIX File",command =change_file).grid(column=0, row=2)
    ttk.Button(frm,text="Unzip PBIX File", command = lambda: unzip_all(file_location=tkinter_var_file_location.get())).grid(column=0,row=3)
    ttk.Button(frm,text="Report Level Measures to CSV",
     command = lambda: main_csv_saver(tkinter_var_file_name.get(),pbix_class.report_level_measures)).grid(column=0, row=4)
    ttk.Button(frm, text="Quit", command=root.quit).grid(column=0, row=5)
    root.mainloop()

pbix_utility_window()