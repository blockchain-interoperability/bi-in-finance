import os
import xmltodict
import json
from collections import defaultdict
from tkinter import filedialog
import tkinter as tk

def read_xml_file(file_path):
    with open(file_path, 'r') as xml_file:
        return xml_file.read()

def convert_xml_to_dict(xml_data):
    return xmltodict.parse(xml_data)


def write_json_file(file_path, data):
    with open(file_path, 'w') as json_file:
        json_file.write(data)


def choose_xml_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Choose an XML file", filetypes=[("XML files", "*.xml")])
    return file_path
    

if __name__ == "__main__":

    xml_data_file = choose_xml_file()
    if not xml_data_file:
        print("No file selected. Exiting.")
        exit()
        
    xml_data = read_xml_file(xml_data_file)

    dict_data = convert_xml_to_dict(xml_data)

    # Converting the final dictionary to JSON
    json_data = json.dumps(dict_data, indent=4)

    output_directory = os.path.dirname(xml_data_file)
    json_out_file = os.path.join(output_directory, os.path.splitext(os.path.basename(xml_data_file))[0] + '.json')

    write_json_file(json_out_file, json_data)