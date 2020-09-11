import pandas
import unicodedata
from sentence_transformers import SentenceTransformer
import scipy.spatial
import pickle as pkl
import re

with open('/content/arc-code-ti-publications.pkl', 'rb') as f:
    pubs = pandas.read_pickle(f)

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)
    
def preprocess_text(sen):

    sentence = str(sen)

    # Removing html tags
    sentence = remove_tags(sentence)

    # Remove hyphenation if at the end of a line
    sentence = sentence.replace('-\n', '')

    # Fix ligatures
    sentence = unicodedata.normalize("NFKD", sentence)

    # Remove punctuations and numbers
    sentence = re.sub('[^a-zA-Z]', ' ', sentence)

    # Single character removal
    sentence = re.sub(r"\s+[a-zA-Z]\s+", ' ', sentence)

    # Removing multiple spaces
    sentence = re.sub(r'\s+', ' ', sentence)

    return sentence

#process text, create model, and sentences
pubs['Text Processed'] = pubs.apply(lambda row: preprocess_text(row['Text']), axis=1)
text_df = pubs[['Text Processed',]].copy()
embedder = SentenceTransformer('bert-base-nli-mean-tokens')
sentences = list(text_df['Text Processed'])

# Eaxmple query sentences
queries = ['How to evolve architecture for constellations and simulation', 'Build behavior of complex aerospace and modeling of safety']
query_embeddings = embedder.encode(queries,show_progress_bar=True)
text_embeddings = embedder.encode(sentences, show_progress_bar=True)

# Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
closest_n = 5
print("\nTop 5 most similar sentences in corpus:")
for query, query_embedding in zip(queries, query_embeddings):
    distances = scipy.spatial.distance.cdist([query_embedding], text_embeddings, "cosine")[0]

    results = zip(range(len(distances)), distances)
    results = sorted(results, key=lambda x: x[1])

    print("\n\n=========================================================")
    print("==========================Query==============================")
    print("===",query,"=====")
    print("=========================================================")

    for idx, distance in results[0:closest_n]:
        print("Score:   ", "(Score: %.4f)" % (1-distance) , "\n" )
        row_dict = pubs.iloc[idx].to_dict()
        print("Title:  " , row_dict["Title"]  , "\n")
        print("Abstract:  " , row_dict["Abstract"] , "\n")
        print("-------------------------------------------")