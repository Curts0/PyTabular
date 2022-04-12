import zipfile
import json
import os
import pandas as pd
from tkinter import filedialog, Tk

import pygetwindow as gw


#pbix_file = filedialog.askopenfilename(title='Select a PBIX File', filetypes=[('Microsoft.MicrosoftPowerBIDesktop','*.pbix')])


class pbix():

    def __init__(self,file_location=None) -> None:
        if file_location is None:
            root = Tk()
            root.wm_attributes('-topmost', 1)
            root.withdraw()
            file_location = filedialog.askopenfilename(title='Select a PBIX File', filetypes=[('Microsoft.MicrosoftPowerBIDesktop','*.pbix')], parent = root)
            print('Got the file name...')
        else:
            pass
        zipping = zipfile.ZipFile(file_location)
        self.zip_object = zipping
        self.file_location = file_location
        self.name_list = self.zip_object.namelist()
        self.layout = json.loads(self.zip_object.open('Report/Layout','r').read().decode('utf-16'))
        self.layout_id = self.layout['id']
        self.layout_theme = self.layout['theme']
        self.layout_report_id = self.layout['reportId']
        self.layout_sections = self.layout['sections']
        self.layout_config = json.loads(self.layout['config'])
        self.layout_filters = pd.DataFrame(json.loads(self.layout['filters']))#self.layout['filters']
        report_level_a = pd.DataFrame(self.layout_config['modelExtensions'][0]['entities']).explode('measures').rename(columns={'name':'table'})
        report_level_b = pd.concat([report_level_a, report_level_a['measures'].apply(pd.Series)],axis=1)
        report_level_c = report_level_b.drop(columns=['extends','measures'])
        self.report_level_measures = report_level_c
        self.report_tabs = pd.DataFrame(self.layout_sections)
        self.number_of_tabs = len(self.report_tabs)
        self.number_of_report_level_measures = len(self.report_level_measures)
        self.number_of_report_level_filters = len(self.layout_filters)
        zipping.close()
        pass
    def __repr__(self) -> str:
        return 'PBIX called... raise the roof'
    def get_read_items(self) -> dict():
        layout_dict = open('Report/Layout','r',encoding='utf-16').read()
        return layout_dict

    def unzip_all(self) -> str():
        try:
            with zipfile.ZipFile(self.file_location) as pbix:
                pbix.extractall()
                return "Extracted Files"
        except:
            return "Invalid file"
    
    




#json_str = "{\"name\":\"8de06175082d21bc6067\",\"layouts\":[{\"id\":0,\"position\":{\"x\":862.9914529914531,\"y\":93.37606837606839,\"z\":13000,\"width\":69.7863247863248,\"height\":30.470085470085472,\"tabOrder\":13000}}],\"singleVisual\":{\"visualType\":\"textbox\",\"drillFilterOtherVisuals\":true,\"objects\":{\"general\":[{\"properties\":{\"paragraphs\":[{\"textRuns\":[{\"value\":\"view by:\"}]}]}}]},\"vcObjects\":{\"background\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}],\"border\":[{\"properties\":{\"show\":{\"expr\":{\"Literal\":{\"Value\":\"false\"}}}}}]}}}"
#json.loads(json_str)
#open('Report\Layout','r',encoding='utf-16 le').read()
#json.loads(json_dict['config'])
#pbix.open('Report/Layout','r').read().decode('utf-16-le')

'''
report

report filters pd.DataFrame(json.loads(a.layout_filters))
page filters
do a file dictionary for some fast facts on the file...

'''