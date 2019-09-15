
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

def from_file(file_path,delimeter=None):
    if delimeter != None:
        file = open(file_path,'r',newline=delimeter)
    else:
        file = open(file_path,'r')
    line = file.readline()
    while line != None and line != '':
        yield line # returns the line with the \n still attched
        line = file.readline()
    file.close()

# --- Modifier Function Generators --

def generator_modifier(source_generator,modifier_function):
    for item in source_generator:
        if item == None:
            yield None
        else:
            yield modifier_function(item)

def make_empty_ent_dict_from_text(source_generator):
    modifier_function = lambda string: { "text":str(string), "ents":[] }
    return generator_modifier(source_generator,modifier_function)

def parse_json_string(source_generator):
    modifier_function = lambda string: json.loads(string)
    return generator_modifier(source_generator,modifier_function)

def dump_json_string(source_generator):
    modifier_function = lambda dict_obj: json.dumps(dict_obj)
    return generator_modifier(source_generator,modifier_function)

def escape_control_chars(source_generator):
    modifier_function = lambda string: string.encode('unicode_escape')
    return generator_modifier(source_generator,modifier_function)

def unescape_control_chars(source_generator):
    modifier_function = lambda string: string.decode('unicode_escape')
    return generator_modifier(source_generator,modifier_function)

def unchars2(source_generator,thing):
    modifier_function = lambda string: string + str(thing)
    return generator_modifier(source_generator,modifier_function)

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
# nexty = make_empty_ent_dict_from_text(unescape_control_chars(escape_control_chars(from_folder('./',filter_by_extension='rc'))))
# next = from_file('README.md')

# print(next(nexty))
# print(next(nexty))
# print(next(nexty))
# print(next(nexty))
# print(next(nexty))
# print(next(unchars2(dump_json_string(nexty),4)))
# print(next(parse_json_string(dump_json_string(nexty))))
# print(next(parse_json_string(dump_json_string(nexty))))
# print(next(parse_json_string(dump_json_string(nexty))))
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



