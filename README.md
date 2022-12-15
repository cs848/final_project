Final Project for CS848 at University of Waterloo
<!-- <<<<<<< HEAD -->
# Extracting Knowledge Graph from text document
<!-- ======= -->
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-360/)  [![Version](https://badge.fury.io/gh/tterb%2FHyde.svg)](https://badge.fury.io/gh/tterb%2FHyde)


A Knowledge Graph (KG) built from text documents may help people and computers to absorb the information in an article by examining the relationships between distinct entities. KGs can also be utilized for other downstream activities like chatbots and QA systems. The state-of-the-art KG construction methods leverage the linguistic features of a sentence, where instead of incorporating all the patterns into the KG, these are first translated to a fixed set of hand- made patterns to extract a relation triple, and then the extracted relation is manually mapped to an existing schema.

In this project, we attempt to enhance two aspects of the previously described system. First, a handcrafted pattern cannot cover every situation of a phrase. To solve this, we can use a dependency tree. We will take the text document and convert it into a dependency tree structure to extract relation triples instead of a pattern-based method. As a preprocessing step, we can first split the text into shorter phrases/clauses and then create a dependency tree out of it.

Second, manually mapping an extracted relation to another relation schema is time-consuming. So, we map the extracted relation triples to an existing KG (e.g., DBpedia). If no mapping is discovered during this matching stage, we will utilize word embedding to determine the similarity between the extracted relation triple and the gold standard in the benchmark in order to choose the highest-rank relation.
 
 ## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
1. Python
2. Spacy (optional)

### Installing
To extract triples from a text document named input.txt, follow the following steps


First download IMoJIE and set up a Python3.6 environment by following the steps given in [link](https://github.com/dair-iitd/imojie/blob/master/README.md).
Once you have got IMoJIE running in your local device, follow these steps to segment the sentences in the input document into multiple independent cluses. 

1) After going in IMoJIE's directory, run the following command to download the pretrained models for clause extraction - 
```bash
$> zenodo_get 3779954
```

2) Then run the following command to get the segmented outputs from input.txt
```bash
$> python standalone.py --inp input.txt --out imojieOutput.txt
```
here imojieOutput.txt contains the corresponding OpenIE extractions. Now we use this imojieOutput file to construct the Knowledge graph.

3) Downloading source code for our model (Text2Triple) by entering the following command in your console to clone the repository.
```bash
$> git clone https://github.com/cs848/final_project.git
```

4) Using a python-3.9 environment and install the dependencies using
```bash
$> pip install -r requirements.txt
```

#### Run the code
To get relation triples using WikiData schema, enter the following command
```bash
$> python make_kg.py -i imojieOutput.txt
```
If you wish to provide your own schema for relation extraction, save the list of allowed terms for relation in a .txt file (here schema.txt) and run the following command to get the corresponding Knowledge Graph
```bash
$> python make_kg.py -i imojieOutput.txt -s schemaFile.txt
```
This produces a result.csv file with the extracted (SUBJECT, RELATION, OBJECT) triples and a result.png file with a graphical representation of the extracted KG

#### Contact
Incase of any issues, please send a mail to ```imohanty@uwaterloo.ca``` or ```l377liu@uwaterloo.ca```
