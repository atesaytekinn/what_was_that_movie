import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import pysolr

solr = pysolr.Solr('http://localhost:8983/solr/movies/', always_commit=True)
status = solr.ping()
# ugly sanity check
if status.split('"status":')[-1][1:3] != "OK":
    print(status)
    raise

tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer() 

def tokens_to_string(token_list):
    rval = ""
    for token in token_list:
        # for removing 's' which is left from possessive's
        if len(token) > 1:
            rval += token
            rval += " "
    return rval.strip()

print("Welcome to the 'What was that Movie?'")
query = input("I am looking for the movie in which: ")

# tokenize and remove punctuation
tokenizer = RegexpTokenizer(r'\w+')
tokens = tokenizer.tokenize(query)
# remove stop-words
filtered_tokens = []
for token in tokens:
    if token not in stop_words:
        filtered_tokens.append(token)
# stem the tokens
stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
# re-build to doc to make it ready for indexing
query = tokens_to_string(stemmed_tokens)

results = solr.search(query)
if len(results) == 0:
    print("Sorry but we could not found any movie for that description :(")
else:
    print("Here are the movies you are probably searching for: ")
    for result in results:
        print(result["id"])

