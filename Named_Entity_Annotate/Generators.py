
import os
import json
from Utilities import write_to_line_number

# --- Source Function Generators --

def from_folder(folder_path,filter_by_extension=None):
    file_list = []
    for filename in os.listdir(folder_path):
        if filter_by_extension == None or filename.endswith(filter_by_extension):
            with open(os.path.join(folder_path,filename),'r') as file:
                yield file.read()

# --- Modifier Function Generators --

def make_empty_ent_dict_from_text(string_source_gen):
    for string in string_source_gen:
        if string == None:
            yield None
        else:
            yield {
                "text":str(string),
                "ents":[]
            }

def parse_json_string(string_source_gen):
    for string in string_source_gen:
        if string == None:
            yield None
        else:
            yield json.loads(string)

def dump_json_string(dict_source_gen):
    for dict_source in dict_source_gen:
        if dict_source == None:
            yield None
        else:
            yield json.dumps(dict_source)

def escape_control_chars(string_source_gen):
    for string in string_source_gen:
        if string == None:
            yield None
        else:
            yield string.encode('unicode_escape')

def unescape_control_chars(string_source_gen):
    for string in string_source_gen:
        if string == None:
            yield None
        else:
            yield string.decode('unicode_escape')

# --- Save Function Generators --

def save_line_to_file(file_path):
    file = open(file_path,'w')
    def save_item(string,item_index):
        if file.closed or string == None:
            file.close()
            return None
        else:
            return Utilities.write_to_line_number(file,string,item_index)
    return save_item

def save_as_file_in_folder(folder_path,output_file_extension):
    def save_item(content_string,item_id):
        file_name = item_id + '.' + output_file_extension
        with open(os.path.join(folder_path,file_name),'w') as file:
            file.write(content_string)
        return True
    return save_item



# nexty = make_empty_ent_dict_from_text(iter([1,2,4]))
nexty = make_empty_ent_dict_from_text(unescape_control_chars(escape_control_chars(from_folder('./',filter_by_extension='rc'))))
# next = from_file('README.md')

# print(next(nexty))
# print(next(nexty))
# print(next(nexty))
# print(next(nexty))
# print(next(nexty))
print(next(dump_json_string(nexty)))
print(next(parse_json_string(dump_json_string(nexty))))
print(next(parse_json_string(dump_json_string(nexty))))
print(next(parse_json_string(dump_json_string(nexty))))
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



