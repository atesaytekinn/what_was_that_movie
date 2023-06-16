import pandas as pd
import nltk

from nltk.tokenize import RegexpTokenizer # better than nltk.word_tokenize() since default tokenizer does not remove punctuation
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer



print("Imports are completed!")

def tokens_to_string(token_list):
    rval = ""
    for token in token_list:
        # for removing 's' which is left from possessive's
        if len(token) > 1:
            rval += token
            rval += " "
    return rval.strip()

df = pd.read_csv("movie_description_corpus_2.csv")
print(f"Shape of the csv: {df.shape}")

title_vals = []
doc_vals = []

tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()  

for ind, row in df.iterrows():
    # tokenize and remove punctuation
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(row["doc"])
    # print(f"Tokens: {tokens}")
    # remove stop-words
    filtered_tokens = []
    for token in tokens:
       if token not in stop_words:
          filtered_tokens.append(token)
    # print(f"Stop-word-filtered tokens: {filtered_tokens}")
    # expand the document
    expansion_tokens = []
    for token in filtered_tokens:
        for syn in wordnet.synsets(token):
            for l in syn.lemmas():
                if (token.lower() != l.name().lower()) and (l.name() not in expansion_tokens) and ("-" not in l.name()) and ("_" not in l.name()):
                    expansion_tokens.append(l.name())
    expanded_tokens = filtered_tokens + expansion_tokens
    # print(f"Expanded  tokens: {expanded_tokens}")
    # stem the tokens
    stemmed_tokens = [stemmer.stem(token) for token in expanded_tokens]
    # print(f"Stemmed tokens: {stemmed_tokens}")
    # re-build to doc to make it ready for indexing
    doc = tokens_to_string(stemmed_tokens)
    # print(f"Doc: {doc}")

    title_vals.append(row["title"])
    doc_vals.append(doc)

df_stem = pd.DataFrame({
    "title" : title_vals,
    "doc" : doc_vals,
})
print(f"Shape of the stemmed csv: {df_stem.shape}")

df_stem.to_csv('movie_description_corpus_expanded_stemmed.csv', encoding='utf-8', index=False)




