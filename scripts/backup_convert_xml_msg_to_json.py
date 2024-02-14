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


def flatten_dict(d, parent_key='', sep='_', cnt=0):
    items = {}
    for k, v in d.items():

        new_key = parent_key + sep + k if parent_key else k

        if isinstance(v, dict):
            key_parts = new_key.split('_')
            if(cnt == 0 and len(key_parts) == 2):
                items.update(flatten_dict(v, '', sep, cnt=1))
            else:
                items.update(flatten_dict(v, new_key, sep, cnt=cnt))
        else:
            items[new_key] = v
    return items


def merge_keys(flattened_dict, n):

    last_level_counts = defaultdict(set)
    for key in flattened_dict.keys():
        parts = key.split('_')
        if(len(parts) < 3):
            continue
        parent_key = '_'.join(key.split('_')[:-1])
        last_level = key.split('_')[-1]
        last_level_counts[parent_key].add(last_level)

    final_merged_dict = {}
    for key, value in flattened_dict.items():
        parent_key = '_'.join(key.split('_')[:-1])
        last_level_count = len(last_level_counts[parent_key])
        if last_level_count > n:
            if parent_key in final_merged_dict:
                final_merged_dict[parent_key].update({key.split('_')[-1]: value})
            else:
                final_merged_dict[parent_key] = {key.split('_')[-1]: value}
        else:
            final_merged_dict[key] = value
    
    return final_merged_dict


def write_json_file(file_path, data):
    with open(file_path, 'w') as json_file:
        json_file.write(data)


def choose_xml_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Choose an XML file", filetypes=[("XML files", "*.xml")])
    return file_path


def group_data_by_prefix(final_merged_dict):

    grouped_data = {}

    for key, value in final_merged_dict.items():
        prefix = key.split('_')[0]
        if prefix not in grouped_data:
            grouped_data[prefix] = {}

        new_key = '_'.join(key.split('_')[1:])
        grouped_data[prefix][new_key] = value

    return grouped_data


if __name__ == "__main__":

    xml_data_file = choose_xml_file()
    if not xml_data_file:
        print("No file selected. Exiting.")
        exit()
        
    xml_data = read_xml_file(xml_data_file)

    dict_data = convert_xml_to_dict(xml_data)

    # flattened_dict = flatten_dict(dict_data)

    # If there are more than N keys with the same 
    # LONG parent name, then merge them into a dictionary
    # N = 2
    # merged_dict = merge_keys(flattened_dict, N)

    # final_dict = group_data_by_prefix(merged_dict)


    # Converting the final dictionary to JSON
    json_data = json.dumps(dict_data, indent=4)

    # json_out_file = os.path.splitext(xml_data_file)[0] + '.json'

    output_directory = os.path.dirname(xml_data_file)
    json_out_file = os.path.join(output_directory, os.path.splitext(os.path.basename(xml_data_file))[0] + '.json')

    write_json_file(json_out_file, json_data)