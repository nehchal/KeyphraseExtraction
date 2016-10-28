import logging

from spacy.en import English


class SpacyNlpUtil:
    nlp = None
    logger = None

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info('Spacy. Fire in the hole.')

    def tagger(self, text):
        response_dict = {}
        if self.nlp is None:
            self.nlp = English(parser=True, tagger=True, entity=True)
        doc = self.nlp(text.decode('utf-8'))
        response_dict['noun_chunks'] = self.get_noun_chunks(doc)
        return response_dict

    @staticmethod
    def get_noun_chunks(doc):
        noun_chunks = {}
        for chunk in doc.noun_chunks:
            chunk_str = str(chunk).strip()
            if chunk_str != "" and "." not in chunk_str:
                noun_chunks[chunk_str] = 1
        return noun_chunks.keys()