import zipfile
import json
import os
import pandas as pd
from tkinter import filedialog, Tk

import pygetwindow as gw


#pbix_file = filedialog.askopenfilename(title='Select a PBIX File', filetypes=[('Microsoft.MicrosoftPowerBIDesktop','*.pbix')])


class pbix():
    def __init__(self,file_location=None) -> None:

        #Get top level .pbix file items
        if file_location is None:
            root = Tk()
            root.wm_attributes('-topmost', 1)
            root.withdraw()
            file_location = filedialog.askopenfilename(title='Select a PBIX File', filetypes=[('Microsoft.MicrosoftPowerBIDesktop','*.pbix')], parent = root)
            print('Got the file name...')
        else:
            pass
        self.zipping = zipfile.ZipFile(file_location)
        self.file_location = file_location
        self.name_list = self.zipping.namelist()

        #Base Layout Items
        self.layout = json.loads(self.zipping.open('Report/Layout','r').read().decode('utf-16'))
        self.layout_id = self.layout['id']
        self.layout_theme = self.layout['theme']
        self.layout_report_id = self.layout['reportId']

        #Report Pages
        self.layout_sections = self.layout['sections']
        self.layout_config = json.loads(self.layout['config'])
        self.layout_filters = pd.DataFrame(json.loads(self.layout['filters']))#self.layout['filters']
        report_level_a = pd.DataFrame(self.layout_config['modelExtensions'][0]['entities']).explode('measures').rename(columns={'name':'table'})
        report_level_b = pd.concat([report_level_a, report_level_a['measures'].apply(pd.Series)],axis=1)
        report_level_c = report_level_b.drop(columns=['extends','measures'])
        self.report_level_measures = report_level_c
        self.report_tabs = pd.DataFrame(self.layout_sections).add_suffix('_report')
        self.number_of_tabs = len(self.report_tabs)
        self.number_of_report_level_measures = len(self.report_level_measures)
        self.number_of_report_level_filters = len(self.layout_filters)
        pass



    def __repr__(self) -> str:
        return 'PBIX called... raise the roof'
    def get_read_items(self) -> dict():
        layout_dict = open('Report/Layout','r',encoding='utf-16').read()
        return layout_dict

    def unzip_all(self,location='working'):
        with self.zipping as pbix:
            pbix.extractall(path=location)
            pbix.close()
            return "Extracted Files"


    