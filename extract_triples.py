import re

def extract_triples(filename, nlp):
    # getting phrases from document
    with open(filename, 'r') as file:
        data = file.read()

    res = re.findall(r'\((.*?)\)', data.replace(";", ""))
    phrases = []
    for s in res:
        phrases.append(" ".join(s.split()).replace(',', ''))

    ## extract triples from spacy dependency tree
    events = []
    for phrase in phrases:

        doc = nlp(phrase)

        root = [token for token in doc if token.head == token][0]

        left_span = doc[root.left_edge.i : root.i]

        entity_list = [a.text for a in doc.ents]

        num_rights = root.n_rights
        n = 0
        while n < num_rights:
            subject = list(root.rights)[n]
            n += 1
            for child in subject.subtree:
                if child.pos_ == 'VERB':
                    root = child
                    num_rights = root.n_rights
                    n = 0
                if child.pos_ == 'NOUN' or child.pos_ == 'PROPN' or child.text in entity_list:
                    lists = []
                    lists.append(left_span.text) #ent1

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

    return new_events
