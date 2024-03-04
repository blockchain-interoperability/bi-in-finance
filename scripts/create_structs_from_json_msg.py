import json
import re
from tkinter import filedialog
import tkinter as tk
import os

def choose_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Choose file", filetypes=[("Json files", "*.json"), ("XML files", "*.xml"), ("XSD files", "*.xsd"), ("All files", "*.*")])
    return file_path


def collect_unique_struct_names(json_data, unique_structs):
    for key, value in json_data.items():
        if isinstance(value, dict):
            unique_structs.add(key)
            collect_unique_struct_names(value, unique_structs)

def sanitize_variable_name(name):
    # Remove special symbols from the beginning of the variable name
    return re.sub(r'^[^a-zA-Z_]+', '', name)

def generate_struct(json_data, struct_name, structs):
    struct_def = f"struct {struct_name} {{\n"
    for key, value in json_data.items():
        if isinstance(value, dict):
            nested_struct_name = sanitize_variable_name(key)  # Remove special symbols
            nested_struct_def = generate_struct(value, nested_struct_name, structs)
            structs[nested_struct_name] = nested_struct_def
            struct_def += f"    {nested_struct_name} {key};\n"
        elif key in unique_structs:
            struct_def += f"    {sanitize_variable_name(key)} {sanitize_variable_name(key)};\n"  # Remove special symbols
        else:
            struct_def += f"    string {sanitize_variable_name(key)};\n"  # Remove special symbols
    
    struct_def += "}\n"
    
    return struct_def

def write_structs_to_file(structs, filename):
    with open(filename, "w") as f:
        for struct in structs.values():
            f.write(struct + "\n")

input_file_path = choose_file()
if not input_file_path:
    print("No file selected. Exiting.")
    exit()


# Read JSON data from file
with open(input_file_path, "r") as f:
    json_data = json.load(f)

# Collect unique struct names
unique_structs = set()
collect_unique_struct_names(json_data['Document'], unique_structs)

# Generate struct definitions
structs = {}
for struct_name in unique_structs:
    generate_struct(json_data['Document'], struct_name, structs)

output_directory = os.path.dirname(input_file_path)
out_file = os.path.join(output_directory, "global_struct_definitions.sol")

# Write struct definitions to file
write_structs_to_file(structs, out_file)
