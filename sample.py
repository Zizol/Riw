from Utils.Loader import *
from Utils.Search import *
import argparse


def indexation():
    Datas = loadData("../CS276/pa1-data/0/")
    frequent_words = [word[0] for word in common_word(Datas, 200)]
    filtered_collection_frequent = remove_stop_words(Datas, frequent_words)
    stemmed_collection = collection_stemming(filtered_collection_frequent)
    lemmatized_collection = collection_lemmatize(stemmed_collection)
    vocabulary_stanford = extract_indexation_vocabulary(lemmatized_collection)
    lemmatized_tokens = {}
    for document in lemmatized_collection:
        lemmatized_tokens[document] = lemmatized_collection[document].upper().split(" ")
    index_inverse = build_inverted_index(lemmatized_tokens, 1)
    index_frequence = build_inverted_index(lemmatized_tokens, 2)
    index_position = build_inverted_index(lemmatized_tokens, 3)
    save_inverted_index_pickle(index_inverse, 'Indexes/inverted_index.pickle')
    save_inverted_index_pickle(index_frequence, 'Indexes/inverted_frequency.pickle')
    save_inverted_index_pickle(index_position, 'Indexes/inverted_position.pickle')
    save_inverted_index_pickle(frequent_words, 'Indexes/frequent_words.pickle')

def recherche(query, model_type):
    index_document = load_inverted_index_pickle("Indexes/inverted_index.pickle")
    index_frequence = load_inverted_index_pickle("Indexes/inverted_frequency.pickle")
    index_position = load_inverted_index_pickle("Indexes/inverted_position.pickle")
    frequent_words = load_inverted_index_pickle("Indexes/frequent_words.pickle")
    with open("../CS276/Queries/dev_queries/query.8") as f:
        requests = {}
        requests[0] = f.read()
    traite = traitement(requests, frequent_words)
    relevance_judgments = load_relevance_judgments('../CS276/Queries/dev_output/8.out', requests)
    vocabulary = {doc for doc in list(index_document.keys())}
    traite_polonaise = {0: transformation_query_to_postfixe(traite[0])}
    result = evaluate_boolean_model(traite_polonaise, index_document, relevance_judgments, "AND")
    with open("Output/8.bonjour" ,"a") as f:
        for query in result:
            f.write(str(query))
            for key in result[query].keys():
                f.write(key)
                f.write(str(result[query][key]))
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("module", choices=["indexation", "recherche"], help="le module à initier")
    parser.add_argument("--query", type=str, default="boolean", help="la requete")
    parser.add_argument("--model_type", choices=["boolean", "vectorial"], default="boolean", help="le type de modèle à utiliser")

    args = parser.parse_args()
    if args.module == "indexation":
        indexation()
    elif args.module == "recherche":
        if not args.query:
            print("il faut au moins une requete")
        else:
            print(recherche(args.query, args.model_type))

