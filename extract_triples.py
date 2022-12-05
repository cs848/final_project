import spacy
import re
from qwikidata.sparql  import return_sparql_query_results
from difflib import SequenceMatcher
# nlp = spacy.load("en_core_web_lg")
# nlp.add_pipe(nlp.create_pipe('merge_noun_chunks'))
# nlp.add_pipe(nlp.create_pipe("merge_entities"))

### "imojie_output.txt" This output file is from IMOJIE's output
with open('output.txt', 'r') as file:
    data = file.read()

res = re.findall(r'\((.*?)\)', data.replace(";", ""))
text_list = []
for s in res:
    text_list.append(" ".join(s.split()).replace(',', ''))
print(text_list)
# ## remove all "," from a sentence
# text_list.append("Barack Obama was born in Honolulu.")
# ## extract triples from spacy dependency tree
# events = []
# for text in text_list:

#     doc = nlp(text)

#     root = [token for token in doc if token.head == token][0]

#     span = doc[root.left_edge.i : root.i]

#     ents_list = [a.text for a in doc.ents]

#     for n in range(root.n_rights):
#         subject = list(root.rights)[n]
#         for child in subject.subtree:
#             if child.pos_ == 'VERB':
#                 root = child
#             if child.pos_ == 'NOUN' or child.pos_ == 'PROPN' or child.text in ents_list:
#                 lists = []
#                 lists.append(span.text) #ent1

#                 lists.append(child.text) #ent2
#                 if child.head.pos_ == 'ADP' and child.head.text != 'of':
#                     lists.append(root.text + " " + child.head.text) #relation
#                 else:
#                     lists.append(root.text)
#                 events.append(lists)