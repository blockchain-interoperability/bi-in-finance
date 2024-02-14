import json
from tkinter import filedialog
import tkinter as tk
import os

def choose_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Choose file", filetypes=[("Json files", "*.json"), ("XML files", "*.xml"), ("XSD files", "*.xsd"), ("All files", "*.*")])
    return file_path


def populate_template(template_data, pacs008_data):
    populated_data = template_data.copy()
    
    for key, value in populated_data.items():
        if isinstance(value, dict):
            populated_data[key] = populate_template(value, pacs008_data.get(key, {}))
        elif value == 'NOT_SPECIFIED' and key in pacs008_data:
            populated_data[key] = pacs008_data[key]
    
    return populated_data

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Read JSON template from file
template_file_path = choose_file()
if not template_file_path:
    print("No file selected. Exiting.")
    exit()

template_data = read_json(template_file_path)

# Read example PACS008 data from file
pacs008_file_path = choose_file()
if not pacs008_file_path:
    print("No file selected. Exiting.")
    exit()
pacs008_data = read_json(pacs008_file_path)

# Populate the template with data from the example PACS008
populated_data = populate_template(template_data, pacs008_data)


# Write the populated JSON to a new file
output_directory = os.path.dirname(template_file_path)
output_file_path = os.path.join(output_directory, "populated_global_pacs008_message.json")

with open(output_file_path, 'w') as output_file:
    json.dump(populated_data, output_file, indent=4)
