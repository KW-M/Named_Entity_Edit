

from Named_Entity_Annotate import Server, Generators

source_generator = Generators.from_folder('questions')

json_modifier = Generators.parse_json_string(source_generator)

save_callback = Generators.save_line_to_file('output.json')

Server.run(avalable_entitiy_labels=["PRODUCT","org","GpE","LOC","MONEY","TIME",],next_example_generator=json_modifier,save_example_callback=save_callback)