from qwikidata.sparql  import return_sparql_query_results
from difflib import SequenceMatcher

def map_relations(events, nlp):

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

    # print("\n### Map to Wikidata ###\n")
    # for e in events:
    #     print(e)

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

    # print("\n###### After Similarity #######\n")
    # for e in events:
    #     print(e)