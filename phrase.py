import spacy
import re
from qwikidata.sparql  import return_sparql_query_results
from difflib import SequenceMatcher
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe(nlp.create_pipe('merge_noun_chunks'))
nlp.add_pipe(nlp.create_pipe("merge_entities"))
#text = "Knowledge Graph is an important resource for humans and machines"

######################################
######################################
######## Triple Extraction Part
######################################
######################################

### "imojie_output.txt" This output file is from IMOJIE's output
with open('output.txt', 'r') as file:
    data = file.read()
res = re.findall(r'\((.*?)\)', data.replace(";", ""))
text_list = []
for s in res:
    text_list.append(" ".join(s.split()).replace(',', ''))
print(text_list)
## remove all "," from a sentence
text_list.append("Barack Obama was born in Honolulu.")
## extract triples from spacy dependency tree
events = []
for text in text_list:

    doc = nlp(text)

    root = [token for token in doc if token.head == token][0]

    span = doc[root.left_edge.i : root.i]

    ents_list = [a.text for a in doc.ents]

    for n in range(root.n_rights):
        subject = list(root.rights)[n]
        for child in subject.subtree:
            if child.pos_ == 'VERB':
                root = child
            if child.pos_ == 'NOUN' or child.pos_ == 'PROPN' or child.text in ents_list:
                lists = []
                lists.append(span.text) #ent1

                lists.append(child.text) #ent2
                if child.head.pos_ == 'ADP' and child.head.text != 'of':
                    lists.append(root.text + " " + child.head.text) #relation
                else:
                    lists.append(root.text)
                events.append(lists)

## remove VERB from ent1, and add it to ent2
## eg. [obama was, honolulu, born in] --> [obama, honolulu, was born in]          
for e in events:
    doc = nlp(e[0])
    for token in doc:
        if token.pos_ == 'VERB':
            e[0] = e[0].replace(token.text, '').strip()
            e[2] = token.text + ' ' + e[2]

for e in events:
    print(e)

for e in events:
    doc = nlp(e[1])
    for a in doc.ents:
        print(a, a.label_)

## merge Location and date as attributes
## remove DATE triples
remove_cand = []
for i in range(len(events)):
    doc = nlp(events[i][1])
    for token in doc.ents:
        if token.text != '' and i != 0:
            if (token.label_ == 'DATE' or token.label_ == 'GPE') and events[i][2].split(" ")[0] == events[i - 1][2].split(" ")[0]:
                if token.label_ == 'GPE':
                    events[i - 1].append("Location: " + events[i][1])
                if (token.label_ == 'DATE'):
                    if i < len(events) - 1: #check for next triple, if it is a DATE from the same sentence, merge together
                        doc1 = nlp(events[i + 1][1])
                        for token_next in doc1.ents:
                            if token_next.label_ == 'DATE' and events[i][2].split(" ")[0] == events[i + 1][2].split(" ")[0]:

                                events[i - 1].append("Time: " + events[i][1] + " - " + events[i+1][1])
                                remove_cand.append(events[i])
                                remove_cand.append(events[i+1])

                    if len(events[i-1]) <= 3: #if events[i-1] has Time attribute, skip this step
                        events[i - 1].append("Time: " + events[i][1])
                        remove_cand.append(events[i])
        else:
            break
new_events = []
for e in events:
    if e not in remove_cand:
        new_events.append(e)

events = new_events

# print("\n###Original Events###\n")
# for e in events:
#     if e not in remove_cand:
#         new_events.append(e)
        
# events = new_events

print("\n###Original Events###\n")
for e in events:
    print(e)

######################################
######################################
######## Relation Mapping Part
######################################
######################################

########################
# query over subject with SPARQL
########################
query_string = """
    SELECT ?propLabel ?bLabel   
    WHERE   {     
        wd:""" + "Q76" + """ ?a ?b.      
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }     
        ?prop wikibase:directClaim ?a . 
}
"""

res = return_sparql_query_results(query_string)
query_list=[]
for row in res["results"]["bindings"]:
   query_list.append(row['propLabel']['value'] + "@" + row['bLabel']['value'])

###################
# if ent2 in events matches the object in query_list,
# replace the relation in query_list to events

# Note: not necessary have to match exactly,
# we use built in method to check similarity, if ratio > 0.7, we consider they match
###################
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


for eve in events:
    for cand in query_list:
        #if similar(eve[1].lower(), cand.split("@")[1].lower()) > 0.7: #use similarity to match
        if eve[1].lower() == cand.split("@")[1].lower(): #use exact match
            eve[2] = cand.split("@")[0]
            eve.append("*")

print("\n### Map to Wikidata ###\n")
for e in events:
    print(e)

#####################
# use spaCy similarity function
# to map the relation to wikidata top 2000 relations
#####################
wikidata_list_relation = ['cites work', 'series ordinal', 'author name string', 'instance of', 'stated in', 'retrieved', 'PubMed ID', 'reference URL', 'publication date', 'title', 'published in', 'page', 'volume', 'apparent magnitude', 'astronomical filter', 'issue', 'catalog code', 'DOI', 'catalog', 'author', 'language of work or name', 'country', 'main subject', 'of', 'located in the administrative territorial entity', 'proper motion', 'point in time', 'determination method', 'coordinate location', 'occupation', 'stated as', 'SIMBAD ID', 'right ascension', 'declination', 'epoch', 'sex or gender', 'constellation', 'found in taxon', 'start time', 'VIAF ID', 'parallax', 'given name', 'date of birth', 'radial velocity', 'ResearchGate publication ID', 'Wikimedia import URL', 'Freebase ID', 'imported from Wikimedia project', 'country of citizenship', 'named as', 'part of', 'GeoNames ID', 'Google Knowledge Graph ID', 'image', 'Entrez Gene ID', 'distance from Earth', 'end time', 'chromosome', 'exact match', 'Commons category', 'subclass of', 'family name', 'parent taxon', 'taxon name', 'taxon rank', 'GNS Unique Feature ID', 'place of birth', 'Elo rating', 'UniProt protein ID', 'described by source', 'collection', 'date of death', 'ORCID iD', 'inception', 'category combines topics', 'location', 'heritage designation', 'applies to jurisdiction', 'located in time zone', 'GND ID', 'postal code', 'educated at', 'WorldCat Identities ID', 'sport', 'follows', 'followed by', 'has part', 'population', 'curator', 'The Peerage person ID', 'Dimensions Publication ID', 'member of sports team', 'official name', 'employer', 'genomic assembly', 'official website', 'copyright status']


def similar_to_wikidata(ent):
    doc1 = nlp(ent)
    relation_dict = {}
    for i in wikidata_list_relation:
        doc2 = nlp(i)
        res = doc1.similarity(doc2)
        relation_dict[i] = res
    #print(relation_dict)
    sorted_values = sorted(relation_dict.values(), reverse = True)
    sorted_dict = {}
    for i in sorted_values:
        for k in relation_dict.keys():
            if relation_dict[k] == i:
                sorted_dict[k] = relation_dict[k]
                break
    return list(sorted_dict.keys())[0] #sorting the similarity value and return the one with the highest score

#from spacy_entity_linker import similar_to_wikidata
for e in events:
    if "*" not in e:
        e[2] = similar_to_wikidata(e[2])

print("\n###### After Similarity #######\n")
for e in events:
    print(e)

######################
# remove duplicate triples
######################
# unique_triple_list =[]

# for i in range(len(events)):
#     for n in range(len(unique_triple_list)):
#         if (events[i][0] not in unique_triple_list[n][0]) and (events[i][1] not in unique_triple_list[n][1]):
#             unique_triple_list.append(events[i])
#         else:
#             continue

# print("\n###### Remove Duplicate #######\n")
# for e in unique_triple_list:
#     print(e)