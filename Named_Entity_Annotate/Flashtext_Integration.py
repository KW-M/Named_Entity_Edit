install_message = """

This integration requires the flashtext module for fast keyword lookups.
Please install it by running:
>  pip install flashtext
        or
>  pip3 install flashtext

"""
try:
    from flashtext import KeywordProcessor
except ModuleNotFoundError:
    print(install_message)

from json import dumps,loads
from Generators import generator_modifier

class flashtext_keyword_class(object):

    # Initialize the flashtext keyword_processor with any passed arguements for example case_sensitive=True
    def __init__(self, *args, **kwargs):
        self.keyword_processor = flashtext.KeywordProcessor(*args, **kwargs)
        self.keyword_save_file_path = './NER_Annotate_Keyword_Save.json'

    def __del__(self):
        self.save_flashtext_keywords()

    def run_keywords_source_modifier(self,source_generator):
        def modifier_function(text_string):
            keywords_found = keyword_processor.extract_keywords(str(text_string),span_info=True)
            keywords_tuple_to_span_function = lambda keyword_tuple: {'label':keyword_tuple[0],'start':keyword_tuple[1],'end':keyword_tuple[2]}
            spans = map(keywords_tuple_to_span_function, keywords_found)
            return { 'text': text_string, 'spans': spans }
        return Generators.generator_modifier(source_generator,modifier_function)

    def update_keywords_save_modifier(self,source_generator):
        None

    def _update_keywords(self,keywords_to_add=[],keywords_to_remove=[]):
        for keyword in keywords_to_add:
            label = keywords_to_add[keyword]
            self.keyword_processor.add_keyword(keyword,label)
        for keyword in keywords_to_remove:
            self.keyword_processor.remove_keyword(keyword)

    def load_flashtext_keywords(self,filepath=None):
        if filepath != None:
            self.keyword_save_file_path = filepath
        with open(self.keyword_save_file_path,'r') as f:
             content = f.read()
        array = json.loads(content)
        self._update_keywords(keywords_to_add=array)

    def save_flashtext_keywords(self,filepath=None):
        if filepath != None:
            self.keyword_save_file_path = filepath
        json = json.dumps(self.keyword_processor.get_all_keywords())
        with open(self.keyword_save_file_path,'w') as f:
             f.write(json)



