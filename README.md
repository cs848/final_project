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

#### Download the source code
Enter the following command in your console to clone the repository.
```bash
$> git clone https://github.com/cs848/final_project.git
```
Once you have the repo cloned, extracting knowledge graphs from natural language text will be done in two steps. 

First, given a sentence, we will segment it into simple independent clauses to help us with entity extraction. To do this, we use [IMoJIE](https://github.com/dair-iitd/imojie). You can read more about it by clicking on the link. 

Follow the following steps to download the pretrained models for sentence segmentation. You would need a Python3.6 environment to run IMoJIE.
```bash
$> cd final_project/iitd_imojie
$> pip install -r requirements.txt
$> zenodo_get 3779954
```

Note: if the ```zenodo_get``` command takes too long to run, you can download it directly from [here](https://zenodo.org/api/files/31736bc8-9c8c-471b-b60b-99cf7c12d24a/imojie_models.tar.gz) and move it to iitd_imojie folder. Remember extract the contents in the folder by clicking on the .tar file. 

Once you have got IMoJIE running in your local device, run the following command to get the segmented outputs from input.txt - 

```bash
$> python standalone.py --inp input.txt --out imojieOutput.txt
```
here imojieOutput.txt contains the corresponding OpenIE extractions. Now we use this imojieOutput file to construct the Knowledge graph.

Once this is done, decativate the Python3.6 environment and using a Python3.9 environment and install the dependencies for Text2Triple by running the following commands - 
```bash
$> cd ..
$> pip install -r requirements.txt
```

#### Run the code
Now, as we have Text2Triple up and running, to get relation triples using WikiData schema, enter the following command
```bash
$> python make_kg.py -i imojieOutput.txt
```
If you wish to provide your own schema for relation extraction, save the list of allowed terms for relation in a .txt file (here schema.txt) and run the following command to get the corresponding Knowledge Graph
```bash
$> python make_kg.py -i imojieOutput.txt -s schemaFile.txt
```
This produces a result.csv file with the extracted (SUBJECT, RELATION, OBJECT) triples and a result.png file with a graphical representation of the extracted KG

The gold standard sentences from New York Times with their corresponding extracted relation triples are in the ```gold_standard.json``` file

Note - While giving file parameters, make sure to input the file path relative to the main project's directory 

#### Contact
Incase of any issues, please send a mail to ```imohanty@uwaterloo.ca``` or ```l377liu@uwaterloo.ca```
