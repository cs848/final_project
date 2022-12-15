import json

#####################
# use spaCy similarity function
# to map the relation to wikidata top 2000 relations
#####################

def get_wikidata(file):
    f = open(file)
    data = json.load(f)
    res = []
    for key in data:
        res.append(data[key])

    return res


def similar_to_wikidata(ent, nlp, wikidata):
    doc1 = nlp(ent)
    relation_dict = {}
    # print(wikidata_list_relation)
    for i in wikidata:
        doc2 = nlp(i)
        res = doc1.similarity(doc2)
        relation_dict[i] = res

    sorted_values = sorted(relation_dict.values(), reverse = True)
    sorted_dict = {}
    for i in sorted_values:
        for k in relation_dict.keys():
            if relation_dict[k] == i:
                sorted_dict[k] = relation_dict[k]
                break
    return list(sorted_dict.keys())[0] #sorting the similarity value and return the one with the highest score


#from spacy_entity_linker import similar_to_wikidata
def map_wiki(events, nlp, schema_file = None):
    if schema_file == None:
        relation_schema = get_wikidata("src/wikiprop.json")
    else:
        with open(schema_file, 'r') as file:
            text = file.read()
        relation_schema = text.split("\n")
    
    for e in events:
        if "*" not in e:
            e[2] = similar_to_wikidata(e[2], nlp, relation_schema)

    triples = []
    subj = []
    reln = []
    obj = []
    for e in events:
        triple = 'SUBJECT: ' + e[0] + ' RELATION: ' + e[2] + ' OBJECT: ' + e[1]
        triples.append(triple)
        subj.append(e[0])
        reln.append(e[2])
        obj.append(e[1])

    return triples, subj, reln, obj
    
