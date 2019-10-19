# Named Entity Annotate

A little tool I made for annotating text to train spaCy's (or any) Named Entity Recognition model.

Note: This library is still a work-in-progress.

## Docs

## Install

```bash
$ pip install NER_Annotate (not avalable yet)
```

### Getting Started

Named_Entity_Annotate's main function is Server.run()

```python
from Named_Entity_Annotate import Server, Generators

source_generator = Generators.parse_json_string(Generators.from_folder('examples'))

save_callback = Generators.save_line_to_file('output.json')

Server.run(
  avalable_entitiy_labels=["PRODUCT","org","GpE","LOC","MONEY","TIME",],
  next_example_generator=source_generator,
  save_example_callback=save_callback
)
```

### Recipies for common functionality

* Get examples from a folder of plain text files:

  ```python
  source_generator = Generators.make_empty_ent_dict_with_text(Generators.from_folder('examples'))
  ```
  
* Get examples from a file where each line is a plain text example:

  ```python
  source_generator = Generators.make_empty_ent_dict_with_text(Generators.from_file('examples.txt'))
  ```
  
* Get examples from a folder where each file is already json formatted like the data format below

  ```python
  source_generator = Generators.parse_json_string(Generators.from_folder('examples'))
  ```

### Methods

### Architecture

Named_Entity_Annotator follows a basic pipeline model. When the WebApp requests a new example, it calls the pipeline ending at the source generator which returns the next example text or json, each generator modifier can modifiy and return the example, until the last generator modifier returns the fully formed json to the Named_Entity_Annotate server and the webapp receives it:

[Annotator WebApp]--< Generator Modifier(Previous Modifier Return Value) << Generator Modifier(Source Generator Return Value) << Source Generator()

When you finish annotating one example in the browser, it sends the json back to the Python & calls your save callback with the json data.

`[Annotator WebApp]--> Save Callback(Saved Data in the JSON format mentioned above)`

### Source Generators

### Source Modifiers
