
import os
import json
from Utilities import write_to_line_number

# --- Source Function Generators --

def from_iterator(iterator):
    def get_next_item():
        try:
            return iterator.__next__()
        except StopIteration:
            return None
    return get_next_item

def from_folder(folder_path):
    file_list = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_list.append(os.path.join(folder_path,filename))
    file_iterator = iter(file_list)

    def get_next_item():
        try:
            file_path = file_iterator.__next__()
            with open(file_path,'r') as file:
                return file.read()
        except StopIteration:
            return None
    return get_next_item

def from_file(file_path):
    file = open(file_path,'r')
    def get_next_item():
        line = None
        if not file.closed:
            line = file.readline()
        if line == None or line.strip() == '':
            file.close()
            return None
        else:
            return line
    return get_next_item

# --- Modifier Function Generators --

def make_empty_ent_dict_from_text(string_source_fn):
    def get_item():
        string = string_source_fn()
        if string == None:
            return None
        else:
            return {
                "text":str(string),
                "ents":[]
            }
    return get_item

def parse_json_string(string_source_fn):
    def get_item():
        string = string_source_fn()
        if string == None:
            return None
        else:
            return json.loads(string)
    return get_item

def dump_json_string(dict_source_fn):
    def get_item():
        dict_source = dict_source_fn()
        if dict_source == None:
            return None
        else:
            return json.dumps(dict_source)
    return get_item

def escape_control_chars(string_source_fn):
    def get_item():
        string = string_source_fn()
        if string == None:
            return None
        else:
            return string.encode('unicode_escape')
    return get_item

def unescape_control_chars(string_source_fn):
    def get_item():
        string = string_source_fn()
        if string == None:
            return None
        else:
            return string.decode('unicode_escape')
    return get_item

# --- Save Function Generators --

def save_line_to_file(file_path):
    file = open(file_path,'w')
    def save_item(string,item_index):
        if file.closed or string == None:
            file.close()
            return None
        else:
            return write_to_line_number(file,string,item_index)
    return save_item



next = make_empty_ent_dict_from_text(from_iterator(iter([1,2,4])))
# next = make_empty_ent_dict_from_text(unescape_control_chars(escape_control_chars(from_folder('./'))))
# next = from_file('README.md')

print(parse_json_string(dump_json_string(next))())
print(dump_json_string(next)())
print(parse_json_string(dump_json_string(next))())
print(parse_json_string(dump_json_string(next))())
print(next())
print(next())
# print(next())
# print(next())
# print(next())
# print(next())
# print(next())
# print(next())
# print(next())
# print(next())
# print(next())
# print(next())



