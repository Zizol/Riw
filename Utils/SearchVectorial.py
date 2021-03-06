from collections import OrderedDict, Counter
import numpy as np
from Utils.Loader import article_word_tokenize, remove_stop_words, collection_lemmatize
from math import *


def remove_non_index_term(query,inverted_index):
    query_filt = []
    for token in query:
        if token in inverted_index:
            query_filt.append(token)
    return query_filt


def pre_processed_query(query,inverted_index, frequent_words):
    tokenized_query = article_word_tokenize(query)
    filt_query = remove_non_index_term(tokenized_query, inverted_index)
    filtered_query = remove_stop_words({"query": " ".join(filt_query)}, frequent_words)
    normalized_query = collection_lemmatize(filtered_query)
    return normalized_query["query"]


def get_idf(term,index_frequence,nb_doc):
    return log(nb_doc/len(index_frequence[term].keys()))


def get_tf(term,doc_ID,index_frequence):
    return index_frequence[term][doc_ID]


def get_tf_normalise(term, doc_ID, index_frequence, stats_collection):
    tf = get_tf(term, doc_ID, index_frequence)
    tf_normalise = 0.5 + 0.5 * (tf / stats_collection[doc_ID]["freq_max"])
    return tf_normalise

def get_tf_logarithme_normalise(term, doc_ID, index_frequence, stats_collection):
    tf = get_tf(term, doc_ID, index_frequence)
    tf_logarithme_normalise = (1 + log(tf)) / (1 + log(stats_collection[doc_ID]["freq_moy"]))
    return tf_logarithme_normalise


def get_tf_logarithmique (term,doc_ID, index_frequence):
    tf = get_tf(term,doc_ID, index_frequence)
    if tf > 0:
        return 1 +log(tf)
    else:
        return 0


def processing_vectorial_query(query, inverted_index, stats_collection, weighting_scheme_document,weighting_scheme_query, frequent_words, frequency_index):
    relevant_docs = {}
    counter_query = Counter()
    query_pre_processed = pre_processed_query(query.upper(), inverted_index, frequent_words)
    nb_doc = stats_collection["nb_docs"]
    norm_query = 0.
    for term in query_pre_processed:
        if term in inverted_index:
            w_term_query = 0.
            counter_query.update([term])
            if weighting_scheme_query == "binary":
                w_term_query = 1
            if weighting_scheme_query == "frequency":
                w_term_query = counter_query[term]
            norm_query = norm_query + w_term_query*w_term_query
            for doc in inverted_index[term]:
                w_term_doc = 0.
                relevant_docs[doc] = 0.
                if weighting_scheme_document == "binary":
                    w_term_doc = 1
                if weighting_scheme_document == "frequency":
                    w_term_doc = get_tf(term, doc, frequency_index)
                if weighting_scheme_document == "tf_idf_normalize":
                    w_term_doc = get_tf_normalise(term, doc, frequency_index, stats_collection) * get_idf(term, frequency_index, nb_doc)
                if weighting_scheme_document == "tf_idf_logarithmic":
                    w_term_doc = get_tf_logarithmique (term, doc, frequency_index) * get_idf(term, frequency_index, nb_doc)
                if weighting_scheme_document == "tf_idf_logarithmic_normalize":
                    w_term_doc = get_tf_logarithme_normalise (term, doc, frequency_index, stats_collection) * get_idf(term, frequency_index, nb_doc)
                relevant_docs[doc] = relevant_docs[doc] + w_term_doc * w_term_query
    ordered_relevant_docs = OrderedDict(sorted(relevant_docs.items(), key=lambda t: t[1], reverse=True))
    return ordered_relevant_docs


def get_stats_document(document):
    counter= Counter()
    for term in document:
        counter.update([term])
    stats={}
    stats["freq_max"] = counter.most_common(1)[0][1]
    stats["unique_terms"] = len(counter.items())
    tf_moy = sum(counter.values())
    stats["freq_moy"] = tf_moy/len(counter.items())
    return stats


def get_stats_collection(collection):
    stats={}
    stats["nb_docs"]=len(collection.keys())
    for doc in collection:
        stats[doc] = get_stats_document(collection[doc])
    return stats


def run_model_and_evaluate(query, inverted_index, model, relevance_judgments, frequent_words, index_frequence):
    evaluation_vectorial_request = {}
    # A completer
    for request in query:
        stat_of_collection = get_stats_collection(inverted_index)
        weighting_scheme_document = model[0]
        weighting_scheme_query = model[1]
        request_with_operator = processing_vectorial_query(query[request], inverted_index, stat_of_collection,
                                                           weighting_scheme_document, frequent_words, weighting_scheme_query, index_frequence)
        results = [0 for i in range(len(request_with_operator))]
        for i, doc in enumerate(request_with_operator):
            if doc in relevance_judgments[request]:
                results[i] = 1
        recall = np.cumsum(results) / len(relevance_judgments[request])
        precision = np.cumsum(results) / len(results)
        evaluation_vectorial_request[request] = {"recall": recall, "precision": precision}

    return request_with_operator, evaluation_vectorial_request
