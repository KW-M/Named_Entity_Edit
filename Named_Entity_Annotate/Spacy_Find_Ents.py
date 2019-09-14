# from flashtext import KeywordProcessor
import spacy
from spacy import displacy
from spacy_lookup import Entity

print("Loading Spacy Models...")
blank_nlp = spacy.blank('en')
en_nlp = spacy.blank('en')
print("Blank en - Done.")
web_md_nlp = spacy.load('en_core_web_md')
print("Web Medium - Done.")
web_lg_nlp = spacy.load('en_core_web_lg')
print("Web Large - Done.")

def return_end_char(entity):
    try:
        return entity.end_char
    except:
        return -1

def merge_ents(lower_priority_ents,source_ents):
    ents = list(source_ents)
    print('source_ents:')
    print(ents)
    print('lower_priority_ents:')
    print(list(lower_priority_ents))
    for low_priority_ent in lower_priority_ents:
        previous_ent = None
        for i,ent in enumerate(list(source_ents)):
            if return_end_char(previous_ent) < low_priority_ent.start_char and low_priority_ent.end_char < ent.start_char:
                try:
                    print(f"({previous_ent} : {previous_ent.start_char},{return_end_char(previous_ent)}) < ({low_priority_ent} : {low_priority_ent.start_char},{low_priority_ent.end_char}) < ({ent} : {ent.start_char},{ent.end_char})")
                except:
                    pass
                ents.insert(i - 1, low_priority_ent)
            previous_ent = ent
        if return_end_char(previous_ent) < low_priority_ent.start_char:
                ents.insert(len(ents), low_priority_ent)
    return ents

def find_ents(text):
    print("Finding Ents in: " + text)

    brands = []
    with open("Named_Entity_Training/brands.list",'r') as f:
        line = f.readline()
        while line != None and line.strip() != '':
            brands.append(line.strip())
            line = f.readline()
    print('Reading Brands - Done')

    products = []
    with open("Named_Entity_Training/products.list",'r') as f:
        line = f.readline()
        while line != None and line.strip() != '':
            products.append(line.strip())
            line = f.readline()
    print('Reading Products - Done')

    brand_entity = Entity(keywords_list=brands,label="ORG",case_sensitive=False)
    product_entity = Entity(keywords_list=brands,label="PRODUCT",case_sensitive=False)
    print('Making Fastext Model - Done')

    try:
        en_nlp.remove_pipe("brand_entity")
        en_nlp.remove_pipe("product_entity")
    except:
        pass
    en_nlp.add_pipe(brand_entity,name="brand_entity")
    en_nlp.add_pipe(product_entity,name="product_entity")

    blank_doc = blank_nlp(text)
    print('Running Flashtext')
    flashtext_doc = en_nlp(text)
    print('Running Spacy Web Medium')
    web_md_doc = web_md_nlp(text)
    print('Running Spacy Web Large')
    web_lg_doc = web_lg_nlp(text)
    print('Spacy Models - Done')

    spans = []
    for ent in merge_ents(web_md_doc.ents,merge_ents(web_lg_doc.ents,flashtext_doc.ents)):
        entity = blank_doc.char_span(ent.start_char, ent.end_char, label=ent.label)
        spans.append(entity)
        for token in entity:  # set values of token attributes
            token._.set('is_entity', True)
            token._.set('canonical', None)

    blank_doc.ents = list(blank_doc.ents) + spans #merge_ents(web_md_doc.ents,)

    for span in spans:
        # Iterate over all spans and merge them into one token. This is done
        # after setting the entities – otherwise, it would cause mismatched
        # indices!
        span.merge()

    return displacy.parse_ents(blank_doc)