# Named Entity Annotate

A little tool I made for annotating text to train spaCy's (or any) Named Entity Recognition model.

Note: This library is still a work-in-progress.

## Docs

### Getting Started

### Methods

Named_Entity_Annotator follows a basic pipeline model. When the WebApp requests a new example, it calls the pipeline of generators al the way down to the source generator which returns the next example text or json, each generator modifier can modifiy and return the example, until the last generator modifier returns the fully formed json to the Named_Entity_Annotate server and the webapp receives it:

`[Annotator WebApp(Last Modifier Return Value - Should be in the JSON format mentioned above)]--< Generator Modifier(Previous Modifier Return Value) << Generator Modifier(Source Genearator Return Value) << Source Generator()`

When you finish one example in the browser, it sends the json back to the Python server and calls your save callback.

`[Annotator WebApp]--> Save Callback(Saved Data in the JSON format mentioned above)`

### Source Generators

### Source Modifiers
