import json
import re

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
    
    struct_def += "};\n"
    
    return struct_def

def write_structs_to_file(structs, filename):
    with open(filename, "w") as f:
        for struct in structs.values():
            f.write(struct + "\n")

# Read JSON data from file
with open("global_pacs008_message.json", "r") as f:
    json_data = json.load(f)

# Collect unique struct names
unique_structs = set()
collect_unique_struct_names(json_data['Document'], unique_structs)

# Generate struct definitions
structs = {}
for struct_name in unique_structs:
    generate_struct(json_data['Document'], struct_name, structs)

# Write struct definitions to file
write_structs_to_file(structs, "global_struct_definitions.sol")
