import zipfile
import json
import pandas as pd
from tkinter import filedialog, Tk

class pbix():
    def __init__(self,file_location=None) -> None:
        self.visual_keys = ['id', 'x', 'y', 'z', 'width', 'height', 'config', 'filters', 'tabOrder', 'query', 'dataTransforms']
        self.layout_keys = ['id', 'reportId', 'theme', 'filters', 'resourcePackages', 'sections', 'config', 'layoutOptimization', 'publicCustomVisuals', 'pods']
        self.layout_sections_keys = ['id', 'name', 'displayName', 'filters', 'ordinal', 'visualContainers', 'objectId', 'config', 'displayOption', 'width', 'height']
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
        self.layout_report_id = self.layout['reportId']
        self.layout_theme = self.layout['theme']
        self.layout_resource_packages = self.layout['resourcePackages']
        self.layout_sections = self.layout['sections']
        self.layout_optimization = self.layout['layoutOptimization']
        self.layout_publicCustomVisuals = self.layout['publicCustomVisuals']
        self.layout_pods = self.layout['pods']
        self.layout_config = json.loads(self.layout['config'])

        #Report Level Filters
        self.layout_filters = pd.DataFrame(json.loads(self.layout['filters']))
        
        #Report Level Measures
        report_level_a = pd.DataFrame(self.layout_config['modelExtensions'][0]['entities']).explode('measures').rename(columns={'name':'table'})
        report_level_b = pd.concat([report_level_a, report_level_a['measures'].apply(pd.Series)],axis=1)
        self.report_level_measures = report_level_b.drop(columns=['extends','measures'])

        #Report Pages
        self.report_tabs = pd.DataFrame(self.layout_sections,columns=self.layout_sections_keys).add_suffix('_report')
        page_level_filters_a = self.report_tabs[['id_report','filters_report']]
        self.page_level_filters = 1

        #Stats
        self.number_of_report_tabs = len(self.report_tabs)
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


    