import ast
import pandas as pd
import pysolr
import time

df = pd.read_csv("movie_description_corpus_expanded_stemmed.csv")

solr = pysolr.Solr('http://localhost:8983/solr/movies/', always_commit=True)
status = solr.ping()
# ugly sanity check
if status.split('"status":')[-1][1:3] != "OK":
    print(status)
    raise

# delete old index
solr.delete(q='*:*')
print("All documents are deleted before expanded indexing!!")

docs_to_index = []

for ind, row in df.iterrows():
    doc_dict = {
        "id" : row["title"],
        "title" : row["doc"]
    }
    docs_to_index.append(doc_dict)

print("Let's starting to index!")
solr.add(docs_to_index)

