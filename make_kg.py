import spacy
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from src.extract_triples import extract_triples
from src.map_relations import map_relations
from src.map_wiki import map_wiki

nlp = spacy.load("en_core_web_lg")
nlp.add_pipe('merge_noun_chunks')
nlp.add_pipe('merge_entities')

outfile = 'output.txt'

events = extract_triples(outfile, nlp)
relns = map_relations(events, nlp)
triples, sub, reln, obj = map_wiki(relns, nlp)

with open('result.csv', 'w') as myfile:
    for triple in triples:
        myfile.write(triple + '\n')


kg_df = pd.DataFrame({'source':sub, 'target':obj, 'edge':reln})

G = nx.from_pandas_edgelist(kg_df, "source", "target", 
                          edge_attr=True, edge_key="edge", create_using=nx.MultiDiGraph())

fig = plt.figure(figsize=(12,12))

el = dict(zip(zip(sub, obj), reln))

pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=el,
    font_color='red'
)
fig.savefig('result.png', dpi=fig.dpi)
plt.show()