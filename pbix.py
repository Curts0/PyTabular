from tokenize import String
import zipfile
import json
import os
import pandas as pd
import xml.etree.ElementTree as ET
from tkinter import filedialog, Tk, ttk, StringVar, Label


class pbix:
    def __init__(self, file_location=None) -> None:
        # Get top level .pbix file items
        if file_location is None:
            file_location = retrieve_pbix_file()
        else:
            pass
        self.zipping = zipfile.ZipFile(file_location)
        self.file_location = file_location
        self.base_file_name = os.path.splitext(
            os.path.basename(self.file_location))[0]
        self.file_list = self.zipping.namelist()
        self.pbix_dict = dict()

        # Gets starting point to unzip, it gets the all of the files and compares to the file_metadata variable below...
        #--------------------------------------#
        for file_name in self.file_list:
            # If file_name is in the top level of file_metadata
            if file_name in file_metadata.keys():
                # example Report/Layout {dictionary contents}
                # If the meta_data says it should run as True
                if file_metadata[file_name]["run"]:
                    # Check if the "name" needs to change like Report/Layout to just Layout
                    pbix_dict_key_name = file_name if file_metadata[file_name]["name"] is None else file_metadata[file_name]["name"]
                    # Add to main dictionary and unzip with metadata driven encoding
                    self.pbix_dict[pbix_dict_key_name] = self.file_get_read_items(location=file_name, encoding=file_metadata[file_name]["encoding"])
                    #---------------------------------------------------------------------#
        self.Version = self.pbix_dict["Version"]
        self.Number_Of_Connections = len(self.pbix_dict["Connections"]["Connections"])
        if self.Number_Of_Connections == 1:
            self.Connection_Name =  self.pbix_dict["Connections"]["Connections"][0]["Name"]
            self.Connection_String = self.pbix_dict["Connections"]["Connections"][0]["ConnectionString"]
            self.Connection_Type = self.pbix_dict["Connections"]["Connections"][0]["ConnectionType"]
        self.Dataset_Id = self.pbix_dict["Connections"]["RemoteArtifacts"][0]['DatasetId']
        self.Report_Id = self.pbix_dict["Connections"]["RemoteArtifacts"][0]['ReportId']
        self.pbix_dict['Layout'] = self.dynamic_layout(self.pbix_dict['Layout'])
    #LAYOUT WORK#
    def dynamic_layout(self,starting_dictionary):
        dictionary_to_run = starting_dictionary
        def dict_depth(my_dict):
            if isinstance(my_dict, dict):
                return 1 + (max(map(dict_depth, my_dict.values())) if my_dict else 0)
            return 0
        def str_dict_check(item):
            try:
                return True,json.loads(item)
            except:
                return False,item
        def list_check(item):
            if isinstance(item,list):
                return True
            return False
        run = dict_depth(dictionary_to_run)
        while run > 0:
            for key in dictionary_to_run:
                str_dict_var = str_dict_check(dictionary_to_run[key])
                if str_dict_var[0] == True:
                    dictionary_to_run[key] = str_dict_var[1]
                    dictionary_to_run[key] = self.dynamic_layout(dictionary_to_run[key])
                if list_check(dictionary_to_run[key]):
                    for item in dictionary_to_run[key]:
                        item = self.dynamic_layout(item)
            run = 0
        return dictionary_to_run



        
    def find_visual_by_id(self,visual_id):
        #self.pbix_dict['Layout']['sections'][x]['visualContainers'][x]['id']
        for section in self.pbix_dict['Layout']['sections']:
            for visual_container in self.pbix_dict['Layout']['sections'][section]['visualContainers']:
                if visual_container['id'] == visual_id:
                    return (self.pbix_dict['Layout']['sections'][section]['displayName'],
                    self.pbix_dict['Layout']['sections'][section]['visualContainers'][visual_container])
        return 1
    pass

    def __repr__(self) -> str:
        return 'PBIX called... raise the roof'

    def file_get_read_items(self, location, encoding):
        pbix_dict = self.zipping.open(location, 'r').read().decode(encoding)
        pbix_dict = json.loads(pbix_dict)
        if location == "Version":
            return float(self.zipping.open(location, 'r').read().decode(encoding))
        return pbix_dict


def read_content_xml(file_location=None):
    if file_location is None:
        file_location = retrieve_pbix_file()
    pbix_class = pbix(file_location)
    content_xml_str = pbix_class.zipping.open(
        '[Content_Types].xml', 'r').read().decode('utf-8-sig')
    content_xml = ET.fromstring(content_xml_str)
    content_list = []
    for x in content_xml:
        try:
            content_list.append(x.attrib['PartName'])
        except:
            pass
    return content_list


def retrieve_pbix_file():
    root = Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()
    file_location = filedialog.askopenfilename(title='Select a PBIX File', filetypes=[
                                               ('Microsoft.MicrosoftPowerBIDesktop', '*.pbix')], parent=root)
    root.quit
    print(f'Got the file location...{file_location}')
    return file_location


def unzip_all(file_location=None, save_location=None):
    if file_location is None:
        print('What file to unzip?...')
        file_location = retrieve_pbix_file()
    if save_location is None:
        root = Tk()
        root.wm_attributes('-topmost', 1)
        root.withdraw()
        save_location_directory = filedialog.askdirectory(
            title='Where do you want to save the files?', parent=root)
        save_location = f'{save_location_directory}/{os.path.splitext(os.path.basename(file_location))[0]}'
        root.quit
    with zipfile.ZipFile(file_location) as pbix:
        pbix.extractall(path=save_location)
        pbix.close()
        os.startfile(save_location)
        print(f'Saved Files to {save_location}')


def main_csv_saver(file_name, file_contents, file_location=None, open_file=True):
    if file_location is None or file_name is None:
        root = Tk()
        root.wm_attributes('-topmost', 1)
        root.withdraw()
        file_location = filedialog.asksaveasfilename(
            title='Save As',
            initialfile=file_name,
            defaultextension=[('CSV files', "*.csv")],
            filetypes=[('CSV files', "*.csv")],
            parent=root)
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
    tkinter_var_file_location = StringVar(root, pbix_class.file_location)
    tkinter_var_file_name = StringVar(root, pbix_class.base_file_name)
    tkinter_main_label_var = StringVar(
        root, f'Do stuff with your PBI File - {pbix_class.file_location}')

    root.title(pbix_class.base_file_name)
    root.wm_attributes('-topmost', 1)
    frm = ttk.Frame(root, padding=200)
    frm.grid()
    main_label = Label(frm, textvariable=tkinter_main_label_var).grid(
        column=0, row=1)

    ttk.Button(frm, text="Change Working PBIX File",
               command=change_file).grid(column=0, row=2)
    ttk.Button(frm, text="Unzip PBIX File", command=lambda: unzip_all(
        file_location=tkinter_var_file_location.get())).grid(column=0, row=3)
    ttk.Button(frm, text="Report Level Measures to CSV",
               command=lambda: main_csv_saver(tkinter_var_file_name.get(), pbix_class.report_level_measures)).grid(column=0, row=4)
    ttk.Button(frm, text="Quit", command=root.quit).grid(column=0, row=5)
    root.mainloop()


file_metadata = {
    "Version": {"run": True, "encoding": "utf-16-le", "name": None},
    "DataMashup": {"run": False},
    "DiagramLayout": {"run": False},
    "Report/Layout": {"run": True, "encoding": "utf-16", "name": "Layout"},
    "Settings": {"run": True, "encoding": "utf-16", "name": None},
    "Metadata": {"run": True, "encoding": "utf-16", "name": None},
    "Report/LinguisticSchema": {"run": False},
    "Connections": {"run": True, "encoding": "utf-8", "name": None},
    "SecurityBindings": {"run": False}
}

# pbix_utility_window()
#'C:/Users/CStallings/Documents/Annual Recurring Revenue Dashboard.pbix'
#a = read_content_xml('C:/Users/CStallings/Documents/Annual Recurring Revenue Dashboard.pbix')
