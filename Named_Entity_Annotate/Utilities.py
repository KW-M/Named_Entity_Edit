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