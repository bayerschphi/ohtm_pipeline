import multiprocessing
import json
from gensim.models import Word2Vec
from sklearn.cluster import MiniBatchKMeans
from sklearn.metrics import silhouette_samples, silhouette_score
import numpy as np
import re
import pandas as pd
from ohtm.settings import *

cores = multiprocessing.cpu_count() # Count the number of cores in a computer

# load_file_name = "OHD_complete_new_raw"
# working_folder = "C:\\Users\\phili\\FAUbox\\Oral History Digital\\Topic Modeling\\main test\\github_test\\"
#
# with open(working_folder + load_file_name) as f:
#     top_dic = json.load(f)

def topic_modeling_w2v(corpus_dictionary, topics: int=0, chunking: bool=True):

    w2v_model = Word2Vec(min_count=20,
                     window=2,
                     vector_size=300,
                     sample=6e-5,
                     alpha=0.03,
                     min_alpha=0.0007,
                     negative=20,
                     workers=cores-1)

    if type(corpus_dictionary) is not dict:
        top_dic = json.loads(corpus_dictionary)
    else:
        top_dic = corpus_dictionary
    if chunking == True:

        chunk_data = []
        for a in top_dic["korpus"]:
            for i in top_dic["korpus"][a]:
                chunk_count = 1
                chunk_text = []
                for n in range(1, (len(top_dic["korpus"][a][i]["sent"]) + 1)):
                    n = str(n)
                    if top_dic["korpus"][a][i]["sent"][n]["chunk"] == chunk_count:
                        chunk_text += top_dic["korpus"][a][i]["sent"][n]["cleaned"]
                        if n == str((len(top_dic["korpus"][a][i]["sent"]))):
                            chunk_data += [[i + " chunk_" + str(chunk_count), chunk_text]]

                    else:
                        chunk_data += [[i + " chunk_" + str(chunk_count), chunk_text]]
                        chunk_count += 1
                        chunk_text = []
                        chunk_text += top_dic["korpus"][a][i]["sent"][n]["cleaned"]
        dataset = []
        for i in chunk_data:
            print(i)
            dataset += [i[1]]

    if chunking == False:

        chunk_data = []
        for a in top_dic["korpus"]:
            for i in top_dic["korpus"][a]:
                for n in top_dic["korpus"][a][i]["sent"]:
                    cleaned_text = top_dic["korpus"][a][i]["sent"][n]["cleaned"]
                    chunk_data.append([i, cleaned_text])
        dataset = []
        for i in chunk_data:
            dataset += [i[1]]

    #print(dataset)
    w2v_model.build_vocab(dataset, progress_per=10000)

    w2v_model.train(dataset, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)

    features = []

    for tokens in dataset:
        zero_vector = np.zeros(w2v_model.vector_size)
        vectors = []
        for token in tokens:
            if token in w2v_model.wv:
                try:
                    vectors.append(w2v_model.wv[token])
                except KeyError:
                    continue
        if vectors:
            vectors = np.asarray(vectors)
            avg_vec = vectors.mean(axis=0)
            features.append(avg_vec)
        else:
            features.append(zero_vector)

    vectorized_docs = features

    X = vectorized_docs
    k = topics
    mb = 500
    print_silhouette_values = False

    """Generate clusters and print Silhouette metrics using MBKmeans

    Args:
        X: Matrix of features.
        k: Number of clusters.
        mb: Size of mini-batches.
        print_silhouette_values: Print silhouette values per cluster.

    Returns:
        Trained clustering model and labels based on X.
    """
    km = MiniBatchKMeans(n_clusters=k, batch_size=mb).fit(X)
    print(f"For n_clusters = {k}")
    print(f"Silhouette coefficient: {silhouette_score(X, km.labels_):0.2f}")
    print(f"Inertia:{km.inertia_}")

    if print_silhouette_values:
        sample_silhouette_values = silhouette_samples(X, km.labels_)
        print(f"Silhouette values:")
        silhouette_values = []
        for i in range(k):
            cluster_silhouette_values = sample_silhouette_values[km.labels_ == i]
            silhouette_values.append(
                (
                    i,
                    cluster_silhouette_values.shape[0],
                    cluster_silhouette_values.mean(),
                    cluster_silhouette_values.min(),
                    cluster_silhouette_values.max(),
                )
            )
        silhouette_values = sorted(
            silhouette_values, key=lambda tup: tup[2], reverse=True
        )
        for s in silhouette_values:
            print(
                f"    Cluster {s[0]}: Size:{s[1]} | Avg:{s[2]:.2f} | Min:{s[3]:.2f} | Max: {s[4]:.2f}"
            )



    topics_words = []
    #topics_weights = []
    for nr, line in enumerate(km.cluster_centers_):
        #topics_weights.append(str(w2v_model.wv.most_similar(line)))
        topics_words.append(w2v_model.wv.most_similar(line, topn=1000))

    for nr, line in enumerate(topics_words):
        print(str(nr) + " " + str(line) + '\n')
    #for nr, line in enumerate(topics_weights):
    #    print(str(nr) + " " + str(line) + '\n')

    centers = km.cluster_centers_
    weight_matrix = []

    for nr_l, line in enumerate(vectorized_docs):
        chunk = []
        for center in centers:
            chunk.append(np.linalg.norm(center - line))
        weight_matrix.append(chunk)

   # es wird das finale dic erstellt mit den drei Kategorien "korpus" = alle Interviews; "weight" = Chunk weight Werte; "words" = Wortlisten der Topics
    # vereinfachen möglich! siehe Gespräch mit Dennis

    for i in range(len(weight_matrix)):
        print(weight_matrix[i])
        if chunk_data[i][0].split(" ")[0][:3] not in top_dic["weight"]:
            top_dic["weight"][chunk_data[i][0].split(" ")[0][:3]] = {}
        if chunk_data[i][0].split(" ")[0] not in top_dic["weight"][chunk_data[i][0].split(" ")[0][:3]]:
            top_dic["weight"][chunk_data[i][0].split(" ")[0][:3]][chunk_data[i][0].split(" ")[0]] = {}
        if chunk_data[i][0].split("_")[1] not in top_dic["weight"][chunk_data[i][0].split(" ")[0][:3]][
            chunk_data[i][0].split(" ")[0]]:
            top_dic["weight"][chunk_data[i][0].split(" ")[0][:3]][chunk_data[i][0].split(" ")[0]][
                chunk_data[i][0].split("_")[1]] = {}
        for top_nr, weight in enumerate(weight_matrix[i]):
            top_dic["weight"][chunk_data[i][0].split(" ")[0][:3]][chunk_data[i][0].split(" ")[0]][
                chunk_data[i][0].split("_")[1]][str(top_nr)] = weight

    # Zuerst werden die Ergebnislisten aus top_words_mallet getrennt, da sie in einer Kette mit "+" aneinandergedliedert sind. (0.000*"zetteln" + 0.000*"salonsozialisten") und an word_list_splittet übergeben
    # anschließend wird das Wort*Wert geflecht getrennt und als Tupel (Wert, Wort) passend zu seinem Topic dem dic übergeben.


    for nr_top, topic in enumerate(topics_words):
        word_list = []
        for word in topic:
            word_list.append([word[1], word[0]])
        top_dic["words"][str(nr_top)] = word_list


    # Abspeichern gewisser meta-daten im top_dic
    top_dic["settings"].update({"processed": True})
    top_dic["settings"].update({"model": "mallet"})
    top_dic["settings"].update({"topics": topics})
    top_dic["settings"].update({"coherence": None})
    top_dic["settings"].update({"average_weight": None})
    top_dic["settings"].update({"min_weight": None})
    top_dic["settings"].update({"max_weight": None})

    return top_dic

#topic_modeling_w2v(top_dic, topics=75, chunking=True)