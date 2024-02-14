import xml.etree.ElementTree as ET
from xml.dom import minidom
import xmlschema
import random
from tkinter import filedialog
import tkinter as tk
import os


def choose_xml_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Choose an XML file", filetypes=[("XML files", "*.xml"), ("XSD files", "*.xsd"), ("All files", "*.*")])
    return file_path


def generate_complex_data(schema_type):
    complex_data = {}
    if schema_type.is_simple() and schema_type.base_type.is_atomic():
        return generate_random_data(schema_type.base_type)
    elif schema_type.is_complex():
        if isinstance(schema_type.content, xmlschema.validators.groups.XsdGroup):
            for elem in schema_type.content.iter_elements():
                if elem.name is None:
                    continue
                elem_name = elem.name.split('}')[-1]
                data = generate_random_data(elem.type)
                if(data == {}):
                    data = "NOT_SPECIFIED"

                attributes = {}
                for attr in elem.attributes.values():
                    attr_name = attr.name.split('}')[-1]  # Remove namespace prefix
                    attributes[attr_name] = generate_random_data(attr.type)
                
                if attributes:
                    complex_data[elem_name] = {"value": data, "attributes": attributes}
                else:
                    complex_data[elem_name] = data
 
    return complex_data



def generate_random_data(schema_type):
    if schema_type is None:
        return None
    if schema_type.is_complex():
        return generate_complex_data(schema_type)
    elif schema_type.is_atomic():
        if schema_type.base_type is None:
            return "NOT_SPECIFIED"
        return generate_random_data(schema_type.base_type)
    else:
        return None





def dict_to_str(d, indent=0):
    if isinstance(d, dict):
        lines = []        
        for k, v in d.items():

            if(isinstance(v, dict) and set(v.keys()) == {'value', 'attributes'}):
                attributes_str = ' '.join([f'{attr_key}="{attr_value}"' for attr_key, attr_value in v['attributes'].items()])
                lines.append(f"{' ' * indent}<{k} {attributes_str}>{v['value']}</{k}>")

            else:
                lines.append(f"{' ' * indent}<{k}>{dict_to_str(v)}</{k}>")
        
        return ''.join(lines)
    else:
        return str(d)



def write_xml_data_to_file(data, filename):
    xml_string = dict_to_str(data)
    xml_pretty_string = minidom.parseString(xml_string).toprettyxml(indent="  ", encoding="UTF-8")
    xml_pretty_string_decoded = xml_pretty_string.decode("UTF-8")
    with open(filename, "w") as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')  # Add XML declaration
        file.write('<Document>\n')  # Add root element
        file.write(xml_pretty_string_decoded.split('\n', 1)[1])  # Write the XML content without the XML declaration
        file.write('\n</Document>')  # Close root element




def generate_xml_data(schema, root_element):
    xml_data = {}
    complex_type = schema.elements[root_element].type.content

    if complex_type.is_empty():
        return xml_data

    for elem in complex_type:
        if isinstance(elem, xmlschema.validators.elements.XsdElement):
            elem_name = elem.name
            elem_type = elem.type
            elem_name = elem_name.split('}')[-1]  # Remove namespace prefix
            xml_data[elem_name] = generate_random_data(elem_type)
    return xml_data




# Load the XSD schema
input_file_path = choose_xml_file()
if not input_file_path:
    print("No file selected. Exiting.")
    exit()

schema = xmlschema.XMLSchema(input_file_path)

# Generate the XML data
generated_xml_data = generate_xml_data(schema, 'Document')

output_directory = os.path.dirname(input_file_path)
out_file = os.path.join(output_directory, 'super_' + os.path.splitext(os.path.basename(input_file_path))[0] + '.xml')


# Write the XML data to a file
write_xml_data_to_file(generated_xml_data, out_file)
