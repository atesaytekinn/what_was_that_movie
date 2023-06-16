# functions to be used by the routes

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

import pysolr

def _tokens_to_string(token_list):
    rval = ""
    for token in token_list:
        # for removing 's' which is left from possessive's
        if len(token) > 1:
            rval += token
            rval += " "
    return rval.strip()


def get_query_results(query_text):

    solr = pysolr.Solr('http://localhost:8983/solr/movies/', always_commit=True)
    status = solr.ping()
    # ugly sanity check
    if status.split('"status":')[-1][1:3] != "OK":
        print(status)
        raise

    tokenizer = RegexpTokenizer(r'\w+')
    stop_words = set(stopwords.words('english'))
    stemmer = PorterStemmer() 

    # tokenize and remove punctuation
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(query_text)
    # remove stop-words
    filtered_tokens = []
    for token in tokens:
        if token not in stop_words:
            filtered_tokens.append(token)
    # stem the tokens
    stemmed_tokens = [stemmer.stem(token) for token in filtered_tokens]
    # re-build to doc to make it ready for indexing
    query = _tokens_to_string(stemmed_tokens)

    results = solr.search(query)
    return results


def convert_results_to_dict(results):
    results_dict = {}
    counter = 1
    for result in results:
        key = f"result_{counter}"
        counter += 1
        results_dict[key] = result["id"]
    return results_dict


