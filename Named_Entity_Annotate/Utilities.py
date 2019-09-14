import tempfile

def write_to_line_number(file_ref,line_string,line_index):
    with tempfile.TemporaryFile('a') as temp_file:
        line = temp_file.readline()
        line_num = 0
        while line != None and line.strip() != '':
            temp_file.write(line)
            if line_num == line_index:
                temp_file.write(line_string)
            line = file_ref.readline()
            line_num += 1

def merge_entities_without_overlaps(existing_entity_list,lower_priority_entity_list):
    ents = existing_entity_list.copy()
    print('source_ents:')
    print(ents)
    print('lower_priority_ents:')
    print(lower_priority_entity_list)
    for low_priority_ent in lower_priority_entity_list:
        for i in range(len(existing_entity_list)):
            previous_existing_ent = existing_entity_list[i - 1] or None
            current_existing_ent = existing_entity_list[i] or None
            # Here we check if the low_priority_ent we want is between the end of the previous_exising_ent and start of the next existing entity (current_existing_ent):
            if previous_existing_ent.get("end",-1) < low_priority_ent.get('start',0) and low_priority_ent.get('end',0) < current_existing_ent.get('start',1000000000000):
                ents.insert(i - 1, low_priority_ent)
    return ents