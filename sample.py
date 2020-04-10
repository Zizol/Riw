from Utils.Loader import *
from Utils.Search import *
from Utils.SearchVectorial import *
import argparse
import os


def indexation(doc_type):
    Datas = {}
    for i in range(len(os.listdir("../CS276/pa1-data/"))):
        print("parsing folder {} for documents...".format(i))
        Datas.update(loadData("../CS276/pa1-data/{}/".format(i), doc_type))
    print("filtering collection...")
    frequent_words = [word[0] for word in common_word(Datas, 50)]
    filtered_collection_frequent = remove_stop_words(Datas, frequent_words)
    print("stemming and lemmatizing collection...")
    stemmed_collection = collection_stemming(filtered_collection_frequent)
    lemmatized_collection = collection_lemmatize(stemmed_collection)
    vocabulary_stanford = extract_indexation_vocabulary(lemmatized_collection)
    lemmatized_tokens = {}
    for document in lemmatized_collection:
        lemmatized_tokens[document] = lemmatized_collection[document].upper().split(" ")
    print("building inverted index...")
    index_inverse = build_inverted_index(lemmatized_tokens, 1)
    index_frequence = build_inverted_index(lemmatized_tokens, 2)
    index_position = build_inverted_index(lemmatized_tokens, 3)
    save_inverted_index_pickle(index_inverse, 'Indexes/inverted_index.pickle')
    save_inverted_index_pickle(index_frequence, 'Indexes/inverted_frequency.pickle')
    save_inverted_index_pickle(index_position, 'Indexes/inverted_position.pickle')
    save_inverted_index_pickle(frequent_words, 'Indexes/frequent_words.pickle')


def recherche(query, model_type, weigth_query, weigth_doc):
    print("loading indexes and request and relevance judgements...")
    index_document = load_inverted_index_pickle("Indexes/inverted_index.pickle")
    index_frequence = load_inverted_index_pickle("Indexes/inverted_frequency.pickle")
    index_position = load_inverted_index_pickle("Indexes/inverted_position.pickle")
    frequent_words = load_inverted_index_pickle("Indexes/frequent_words.pickle")
    with open(query) as f:
        requests = {}
        requests[0] = f.read()
    traite = traitement(requests, frequent_words)
    relevance_judgments = load_relevance_judgments('../CS276/Queries/dev_output/{}.out'.format(query[-1]), requests, model_type)
    vocabulary = {doc for doc in list(index_document.keys())}
    print("processing query...")
    print(traite[0])
    if model_type == "boolean":
        results, evaluation = evaluate_boolean_model({0: traite[0].split()}, index_document, relevance_judgments, "AND")
    else:
        results, evaluation = run_model_and_evaluate({0: traite[0]}, index_document, [weigth_doc, weigth_query], relevance_judgments, frequent_words, index_frequence)
    print("printing output...")
    print(results)
    with open("Output/{}.{}_results({}-{})".format(query[-1], model_type, weigth_query, weigth_doc), "a") as file:
        for result in results:
            file.write(result)
    print(evaluation)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("module", choices=["indexation", "recherche"], help="le module à initier")
    parser.add_argument("--doc_type", choices=["html", "php", "all"], default="html", help="le type de fichier à indexer, si on ne veut pas tous les indexer et prendre du temps. Bien sur plus on prend de fichier et plus la recherche est efficace")
    parser.add_argument("--query", type=str, help="la requete")
    parser.add_argument("--model_type", choices=["boolean", "vectorial"], default="boolean", help="le type de modèle à utiliser")
    parser.add_argument("--weigth_query", choices=["binary", "frequency"], default="binary",
                        help="la strategie de poids de la query pour le modèle vectoriel")
    parser.add_argument("--weigth_doc", choices=["binary", "frequency", "tf_idf_normalize", "tf_idf_logarithmic", "tf_idf_logarithmic_normalize"], default="binary",
                        help="la strategie de poids des documents pour le modèle vectoriel")

    args = parser.parse_args()
    if args.module == "indexation":
        indexation(args.doc_type)
    elif args.module == "recherche":
        if not args.query:
            print("il faut au moins une requete : utilisez les documents dans dev_queries")
        else:
            recherche(args.query, args.model_type, args.weigth_query, args.weigth_doc)
