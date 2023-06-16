import ast
import pandas as pd
import pysolr
import time

df = pd.read_csv("movie_description_corpus_stemmed.csv")

solr = pysolr.Solr('http://localhost:8983/solr/movies/', always_commit=True)
status = solr.ping()
# ugly sanity check
if status.split('"status":')[-1][1:3] != "OK":
    print(status)
    raise

docs_to_index = []

for ind, row in df.iterrows():
    doc_dict = {
        "id" : row["title"],
        "title" : row["doc"]
    }
    docs_to_index.append(doc_dict)

print("Let's starting to index!")
# solr.add(docs_to_index)

'''counter = 0
for doc in docs_to_index:
    solr.add([{"id": "doc_1", "title": "A test document",}])
    if counter % 1000 == 0:
        print(f"processing {doc['id']}...") # to understand code is not stucked 
    counter += 1
    time.sleep(0.01)'''



# solr.add([{"id": "doc_1", "title": "A test document",}])

