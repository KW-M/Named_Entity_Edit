# Named Entity Annotate

A little tool I made for annotating text to train spaCy's (or any) Named Entity Recognition model.

Note: This library is still a work-in-progress.

## Docs

### Getting Started

```python

from Named_Entity_Annotate import Server, Generators
# We first use a source Generator
source_generator = Generators.from_folder('/Users/kyle/Desktop/questions')

json_modifier = Generators.parse_json_string(source_generator)

save_callback = Generators.save_line_to_file('/Users/kyle/Desktop/output.json')

Server.run(avalable_entitiy_labels=["PRODUCT","org","GpE","LOC","MONEY","TIME",],next_example_generator=json_modifier,save_example_callback=save_callback)
```

### Recipies for common functionality

```python

```

### Methods

### Architecture

Named_Entity_Annotator follows a basic pipeline model. When the WebApp requests a new example, it calls the pipeline ending at the source generator which returns the next example text or json, each generator modifier can modifiy and return the example, until the last generator modifier returns the fully formed json to the Named_Entity_Annotate server and the webapp receives it:

[Annotator WebApp]--< Generator Modifier(Previous Modifier Return Value) << Generator Modifier(Source Generator Return Value) << Source Generator()

When you finish annotating one example in the browser, it sends the json back to the Python & calls your save callback with the json data.

`[Annotator WebApp]--> Save Callback(Saved Data in the JSON format mentioned above)`

### Source Generators

### Source Modifiers
