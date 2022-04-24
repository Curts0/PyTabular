from tokenize import String
import zipfile
import json
import os
import pandas as pd
import xml.etree.ElementTree as ET
from tkinter import filedialog, Tk, ttk, StringVar, Label


class pbix:
    def __init__(self, file_location=None) -> None:
        def try_recursive(location, initial_try):
            try:
                return location[initial_try]
            except:
                return None

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

        pass

    def __repr__(self) -> str:
        return 'PBIX called... raise the roof'

    # Garbage Functions to Remove or Fix
    def get_read_items(self) -> dict():
        layout_dict = open('Report/Layout', 'r', encoding='utf-16').read()
        return layout_dict


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
    "/Version": {"run": True, "content": [
        {"file_type": "text",
         "decode": "utf-16",
         "contents": "integer",
         "location": "",
         "dictionary_attribute_name": "version"
         }
    ]
    },
    "/DataMashup": {"run": False},
    "/DiagramLayout": {"run": False},
    "/Report/Layout": {
        "run": True,
        "file_type": "json",
        "decode": "utf-16",
        "content": {
            "id": "integer",
            "reportId": "integer",
            "theme": "string",
            "filters": {"file_type": "json_string"}
        }
    },
    "/Settings": {"run": False},
    "/Metadata": {"run": False},
    "/Report/LinguisticSchema": {"run": False},
    "/Connections": {"run": False},
    "/SecurityBindings": {"run": False}
}


# pbix_utility_window()
#'C:/Users/CStallings/Documents/Annual Recurring Revenue Dashboard.pbix'
a = read_content_xml(
    'C:/Users/CStallings/Documents/Annual Recurring Revenue Dashboard.pbix')
