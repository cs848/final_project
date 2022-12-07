import spacy
import re
from qwikidata.sparql  import return_sparql_query_results
from difflib import SequenceMatcher
from extract_triples import extract_triples
from map_relations import map_relations

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe('merge_noun_chunks')
nlp.add_pipe('merge_entities')

outfile = 'output.txt'

events = extract_triples(outfile, nlp)
# print(events)
# print()
relns = map_relations(events, nlp)
print(relns)