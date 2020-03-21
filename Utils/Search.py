from Utils.Loader import article_word_tokenize, remove_stop_words, collection_stemming, collection_lemmatize
import numpy as np

def load_relevance_judgments(filename, requests):
    relevance_judgments = {}
    # A completer
    with open(filename) as f:
        doc = f.readlines()
        for request in requests:
            relevance_judgments[request] = []
            for line in doc:
                if line[0] == str(0):
                    relevance_judgments[request].append(line[2:].rstrip('\n'))
    return relevance_judgments

def traitement(requetes, stop_words):
    requetes_tokenize = {}
    for request in requetes:
        requetes_tokenize[request] = " ".join(article_word_tokenize(requetes[request]))
    requetes_stop = remove_stop_words(requetes_tokenize, stop_words)
    requetes_lemmatize = collection_stemming(requetes_stop)
    traites = collection_lemmatize(requetes_lemmatize)
    return traites

from tt import BooleanExpression


def transformation_query_to_postfixe(query):
    b = BooleanExpression(query)
    return b.postfix_tokens

def transformation_lem_query_to_boolean(query):
    boolean_query=[]
    for token in query:
        boolean_query.append(token)
        boolean_query.append('AND')
    boolean_query.pop()
    return boolean_query

def merge_and_postings_list(posting_term1,posting_term2):
    result=[]
    n = len(posting_term1)
    m = len(posting_term2)
    i = 0
    j = 0
    while i < n and j <m:
        if posting_term1[i] == posting_term2[j]:
            result.append(posting_term1[i])
            i = i+1
            j = j+1
        else:
            if posting_term1[i] < posting_term2[j]:
                i = i+1
            else:
                j=j+1
    return result

def boolean_operator_processing_with_inverted_index(BoolOperator,posting_term1,posting_term2):
    result=[]
    if BoolOperator == "AND":
        result.append(merge_and_postings_list(posting_term1,posting_term2))
    elif BoolOperator=="OR" :
        result.append(merge_or_postings_list(posting_term1,posting_term2))
    elif BoolOperator == "NOT":
        result.append(merge_and_not_postings_list(posting_term1,posting_term2))
    return result

def processing_boolean_query_with_inverted_index(booleanOperator,query, inverted_index):
    relevant_docs = {}
    evaluation_stack = []
    for term in query:
        if term.upper() not in booleanOperator:
            evaluation_stack.append(inverted_index[term.upper()])
        else:
            if term.upper() == "NOT":
                operande= evaluation_stack.pop()
                eval_prop = boolean_operator_processing_with_inverted_index(term.upper(), evaluation_stack.pop(),operande)
                evaluation_stack.append(eval_prop[0])
                evaluation_stack.append(eval_prop[0])
            else:
                operator = term.upper()
                eval_prop =  boolean_operator_processing_with_inverted_index(operator, evaluation_stack.pop(),evaluation_stack.pop())
                evaluation_stack.append(eval_prop[0])
    return  evaluation_stack.pop()

def evaluate_boolean_model(requests, collection_index, relevance_judgments, BooleanOperator):
    evaluation_boolean = {}
    # A completer
    for request in requests:
        boolean_request = transformation_lem_query_to_boolean(requests[request])
        result = []
        for word in boolean_request:
            #if not(word == "U.S" or word.upper() not in vocabulary or word is int):
            result.append(word)
        request_with_operator = processing_boolean_query_with_inverted_index(BooleanOperator, result, collection_index)
        results = [0 for i in range(len(request_with_operator))]
        for i, doc in enumerate(request_with_operator):
            if doc in relevance_judgments[request]:
                results[i] = 1
        recall = np.cumsum(results) / len(relevance_judgments[request])
        precision = np.cumsum(results) / len(results)
        F1 = 2 / ((1 / precision) + (1 / recall))
        beta = .5
        Fb = (1 + beta ** 2) * precision * recall / (beta ** 2 * precision * recall)
        evaluation_boolean[request] = {"recall": recall, "precision": precision, "F1": F1, "Fb": Fb}
    return evaluation_boolean