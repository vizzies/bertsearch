from sentence_transformers import SentenceTransformer, util
import numpy as np
import pickle, pandas
import nltk
nltk.download('punkt')

import sys

embedder = SentenceTransformer('/Users/etyates/Desktop/distilbert-base-nli-mean-tokens')

f = open("/Users/etyates/Desktop/arc-code-ti-publications.pkl", "rb")
corpus_dataframe = pickle.load(f)
f.close()


doc_id_to_sentences = {}
sentence_id_to_doc_id = {}
all_sentences = []
tot_sentences = 0

for ind, row in corpus_dataframe.iterrows():
    
    doc_id = ind

    doc_id_to_sentences.update({doc_id: {}})

    link = row[0]
    try:
        text = row[1]
        text_tok = nltk.sent_tokenize(text)
        all_sentences.extend(text_tok)

    except TypeError as e: pass
    except AttributeError: pass

    try:
        abstract = row[3]
        abstract_tok = nltk.sent_tokenize(abstract)
        all_sentences.extend(abstract_tok)
    except TypeError as e: pass
    except AttributeError: pass

    try:
        title = row[5]
        title_tok = nltk.sent_tokenize(title)
        all_sentences.extend(title_tok)
    except TypeError as e: pass
    except AttributeError: pass

    try:
        authors = row[6]
        authors_l = authors.split(",")
        all_sentences.extend(authors_l)
    except TypeError as e: pass
    except AttributeError: pass
    
    try:
        publisher = row[7]
        pub_clean = publisher.replace("Published at:", "").replace(";", ":")
        pub_components = pub_clean.split(":")
        all_sentences.extend(pub_components)
    except TypeError as e: pass
    except AttributeError: pass
    abstract_length = row[4]
    
    date = row[8]
    all_sentences.append(date)

    for ind, sentence in enumerate(all_sentences):
        tot_sentences += 1
        sentence_id = tot_sentences

        doc_id_to_sentences.get(doc_id).update({sentence_id: sentence})
        sentence_id_to_doc_id.update({sentence_id: doc_id})

print(tot_sentences)

print("ENCODING SENTENCES")
corpus_embeddings = embedder.encode(all_sentences, convert_to_tensor=True, show_progress_bar=True)

query = "man"

# Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
top_k = 5
print("QUERYING")
query_embedding = embedder.encode(query, convert_to_tensor=True, show_progress_bar=True)

print("RUNNING SEM SEARCH")
cos_scores = util.semantic_search(query_embedding, corpus_embeddings)[0]
print("DONE")
# print(cos_scores)
# for score in cos_scores:
#     print(lookup[score["corpus_id"]], score["score"])