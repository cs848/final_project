from qwikidata.sparql  import return_sparql_query_results
from difflib import SequenceMatcher
import itertools
from collections import defaultdict

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def close(a, b, threshold):
    a = str(a.lower())
    b = str(b.lower())
    if a == b:
        return True
    elif similar(a,b) >= threshold:
        return True
    else:
        return False

def get_wikiID(text):
    if text:
        try:
            string = '"' + text + '"' + "@en"
            query = """
                        PREFIX wd: <http://www.wikidata.org/entity/>
                        SELECT DISTINCT ?qid
                        WHERE {

                        ?item rdfs:label """ + string + """ .

                        BIND(STRAFTER(STR(?item), STR(wd:)) AS ?qid) .

                        }
                    """

            res = return_sparql_query_results(query)
            qid = ""
            if res:
                qids = res['results']['bindings']
                if qids:
                    qid = qids[0]['qid']['value']
            return qid
        except:
            return ""
    else:
        return ""

def get_properties(wid):
    res = {}
    try:
        if wid:
            query = """
                        SELECT ?propLabel ?bLabel   
                        WHERE   {     
                            wd:""" + wid + """ ?a ?b.      
                            SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }     
                            ?prop wikibase:directClaim ?a . 
                                }
                    """ 
            res = return_sparql_query_results(query)
    except:
        return {}
    return res

def map_relations(events, nlp):
    
    for event in events:
        new_relns = []
        wids = {}
        for n in range(len(event)):
            if n == 2:
                continue
            string = event[n]
            if "Location" in string:
                wid = get_wikiID(string.replace("Location: ", ""))
            elif "Time" in string:
                continue
            else:
                wid = get_wikiID(string)

            if wid:
                wids[string] = wid

        for key, val in wids.items():
            props = get_properties(val)
            if props:
                for prop in props["results"]["bindings"]:
                    if key not in event[0]:
                        if close(event[0], prop['bLabel']['value'], 0.9):
                            new_reln = [key, event[0], prop['propLabel']['value']]
                            if len(event) > 3:
                                ex_prop = event[3:]
                                new_reln.extend(ex_prop)
                            new_relns.append(new_reln)
                    if key not in event[1]:
                        if close(event[1], prop['bLabel']['value'], 0.9):
                            new_reln = [key, event[1], prop['propLabel']['value']]
                            if len(event) > 3:
                                ex_prop = event[3:]
                                new_reln.extend(ex_prop)
                            new_relns.append(new_reln)
                    if len(event) > 3 and key not in event[3]:
                        if close(event[0], prop['bLabel']['value'], 0.9):
                            new_reln = [key, event[0], prop['propLabel']['value']]
                            new_relns.append(new_reln)
                        if close(event[1], prop['bLabel']['value'], 0.9):
                            new_reln = [key, event[1], prop['propLabel']['value']]
                            new_relns.append(new_reln)

    events += new_relns

    return events