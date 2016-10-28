# KeyphraseExtraction
Keyphrase extraction using Word2vec and Page rank

## Getting started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
* [Spacy](https://spacy.io/)
* [Networkx](https://networkx.github.io/)
* Word2vec vectors trained on Wikipedia data
* Stopwords and topic-file have been added to repository

## Running
```
python SgRank.py
python SemRank.py
```
## Algorithm description
Extract noun chunks using Spacy. Apply pagerank on graph with noun chunks as nodes and edge weights can either be calculated using syntax heuristics or semantic similarity or both.
