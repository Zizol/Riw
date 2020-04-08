import os
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.stem import PorterStemmer
from collections import OrderedDict
import pickle


def loadData(directoryname, doc_type):
    corpus = {}
    for file in os.listdir(directoryname):
        if file.split('.')[-1] == doc_type or doc_type == "all":
            with open(directoryname + file, 'r') as f:
                # A completer
                doc = f.readlines()
                corpus[directoryname[-2:] + file] = doc[0]

    return (corpus)


def article_word_tokenize(text):
    if type(text) != str:
        raise Exception("The function takes a string as input data")
    else:
        # A COMPLETER
        tokens = word_tokenize(text)
        stops = ['.', ',']
        for stop in stops:
            while stop in tokens:
                del tokens[tokens.index(stop)]
        return tokens


def count_frequency(collection):
    # A completer
    tokens_count = Counter()
    for doc in collection.keys():
        tokens = collection[doc].split()
        tokens_count += Counter(tokens)
    return tokens_count


def common_word(collection, n):
    return count_frequency(collection).most_common(n)


def visualize_collection_common(collection, n):
    common_words = common_word(collection, n)
    corpus_common_words = [word[0] for word in common_words]
    corpus_common_counts = [word[1] for word in common_words]

    plt.style.use('dark_background')
    plt.figure(figsize=(15, 12))

    sns.barplot(x=corpus_common_counts, y=corpus_common_words)
    plt.title('Most Common Tokens in the Stanford Corpus');


def remove_stop_words(collection, stop_word_file):
    # TO COMPLETE
    collection_filtered = {}
    for doc in collection.keys():
        tokens = collection[doc].split()
        for stop in stop_word_file:
            while stop in tokens:
                del tokens[tokens.index(stop)]
        tokens = " ".join(tokens)
        collection_filtered[doc] = tokens

    return collection_filtered


def collection_stemming(segmented_collection):
    stemmer = PorterStemmer () # initialisation d'un stemmer
    stemmed_collection = {}
    # a completer
    for doc in segmented_collection.keys():
        tokens = segmented_collection[doc].split(' ')
        stemmed_words = [stemmer.stem(word) for word in tokens]
        stemmed_string = " ".join(stemmed_words)
        stemmed_collection[doc] = stemmed_string
    return stemmed_collection


def collection_lemmatize(segmented_collection):
    stemmer = WordNetLemmatizer () # initialisation d'un lemmatiseur
    # a completer
    lemmatized_collection = {}
    # a completer
    for doc in segmented_collection.keys():
        tokens = segmented_collection[doc].split(' ')
        lemmatized_words = [stemmer.lemmatize(word) for word in tokens]
        lemmatized_string = " ".join(lemmatized_words)
        lemmatized_collection[doc] = lemmatized_string
    return lemmatized_collection


def extract_indexation_vocabulary(processed_collection):
    vocabulary = set()
    # a completer
    for doc in processed_collection.keys():
        vocabulary.update(processed_collection[doc].split(" "))
    return vocabulary


def build_inverted_index(collection, type_index):
    # On considère ici que la collection est pré-traitée
    inverted_index = OrderedDict()
    if type_index == 1:
        for document in collection:
            for term in collection[document]:
                if term in inverted_index.keys():
                    if document not in inverted_index[term]:
                        inverted_index[term].append(document)
                else:
                    inverted_index[term] = [document]
    elif type_index == 2:
        for document in collection:
            for term in collection[document]:
                if term in inverted_index.keys():
                    if document in inverted_index[term].keys():
                        inverted_index[term][document] = inverted_index[term][document] + 1
                    else:
                        inverted_index[term][document] = 1
                else:
                    inverted_index[term] = OrderedDict()
                    inverted_index[term][document] = 1
    elif type_index == 3:
        for document in collection:
            n = 0
            for term in collection[document]:
                n = n + 1
                if term in inverted_index.keys():
                    if document in inverted_index[term].keys():
                        inverted_index[term][document][0] = inverted_index[term][document][0] + 1
                        inverted_index[term][document][1].append(n)
                    else:
                        inverted_index[term][document] = [1, [n]]
                else:
                    inverted_index[term] = OrderedDict()
                    inverted_index[term][document] = [1, [n]]

    return inverted_index


# Ecriture sur disque
def save_inverted_index_pickle(inverted_index, filename):
    with open(filename, "wb") as f:
        pickle.dump(inverted_index, f)
        f.close()


# Chargement
def load_inverted_index_pickle(filename):
    with open(filename, 'rb') as fb:
        index = pickle.load(fb)
        return index
