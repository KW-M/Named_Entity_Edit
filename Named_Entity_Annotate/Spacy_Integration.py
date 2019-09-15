install_message = """

This integration uses the spacy and displacy module for named_entity_recodition.
Please install it by running:
>  pip install spacy
        or
>  pip3 install spacy

"""
try:
    from spacy import displacy
except ModuleNotFoundError:
    print(install_message)

from Generators import generator_modifier

# -- Generator Modifiers --

# Takes in a text generator (eg one of the source generators) and outputs a formatted dict with text and spans attributes
def apply_spacy_model(source_generator,spacy_nlp_model):
    modifier_function = lambda text_string: displacy.parse_ents(spacy_nlp_model(str(text_string)))
    return Generators.generator_modifier(source_generator,modifier_function)