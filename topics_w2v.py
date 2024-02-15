import multiprocessing
import json
from gensim.models import Word2Vec
from sklearn.cluster import MiniBatchKMeans
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_samples, silhouette_score
import numpy as np
import re
import pandas as pd
import umap


#load_file_name = "OHD_complete_new_raw"
#working_folder = "C:\\Users\\moebusd\\sciebo - Möbus, Dennis (moebusd@fernuni-hagen.de)@fernuni-hagen.sciebo.de\\OHD\\Data TM OHD\\"

#with open(working_folder + load_file_name) as f:
#    top_dic = json.load(f)

def topic_modeling_w2v(corpus_dictionary, topics: int=0, chunking: bool=True):
    cores = multiprocessing.cpu_count()  # Count the number of cores in a computer

    w2v_model = Word2Vec(min_count=20,
                     window=2,
                     vector_size=50,
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
                chunk_count = 0
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
            #print(i)
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
    print('Vocab built')

    w2v_model.train(dataset, total_examples=w2v_model.corpus_count, epochs=300, report_delay=1)
    print('Embeddings trained'
          )



    features = [] # Hierarchische Liste, um Chunks aufrechtzuerhalten
    features_avg = [] # Durchschnittswerte für Chunks

    for tokens in dataset:
        #print(tokens)
        zero_vector = np.zeros(w2v_model.vector_size)
        vectors = []
        for token in tokens:
            #print(token)
            if token in w2v_model.wv:
                try:
                    vectors.append(w2v_model.wv[token])
                except KeyError:
                    print('KeyError: ' + str(token))
                    continue
        if vectors:
            features.append(vectors) # jeder Vektor (Wort) eines jeden Chunks in einer Liste
            vectors = np.asarray(vectors) # hier werden die Chunks summiert
            avg_vec = vectors.mean(axis=0) # und ein Mittelwert berechnet
            features_avg.append(avg_vec)
        else:
            features_avg.append(zero_vector)
            features.append([zero_vector])

    vectorized_docs_flat = []

    for chunk in features:
        for feature in chunk:
            vectorized_docs_flat.append(feature)

    vectorized_docs_flat = np.asarray(vectorized_docs_flat)

    vectorized_docs = features

    ## Dimension Reduction
    ## UMAP

    #reducer = umap.UMAP()
    #embedding = reducer.fit_transform(vectorized_docs_flat)

    ##tsne
    embedding = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=30, n_iter=300, verbose=1).fit_transform(vectorized_docs_flat)
    np.save("C:\\Users\\moebusd\\sciebo - Möbus, Dennis (moebusd@fernuni-hagen.de)@fernuni-hagen.sciebo.de\\OHD\\Data TM OHD\\tsne.npy", embedding)
    print(embedding)

    print(len(vectorized_docs))
    print(len(vectorized_docs_flat))
    print(vectorized_docs[:3])
    print(vectorized_docs_flat[:3])

    X = embedding
    k = topics
    mb = 1000
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
    km = MiniBatchKMeans(n_clusters=k, batch_size=mb, verbose=1).fit(X)


    print('Clustering completed, processing output')
    topics_words = []
    #topics_weights = []
    for nr, line in enumerate(km.cluster_centers_):
        print(line)
        #topics_weights.append(str(w2v_model.wv.most_similar(line)))
        topics_words.append(w2v_model.wv.most_similar(line, topn=100))
        print(w2v_model.wv.most_similar(line, topn=10))

    #for nr, line in enumerate(topics_words):
        #print(str(nr) + " " + str(line) + '\n')
    #for nr, line in enumerate(topics_weights):
    #    print(str(nr) + " " + str(line) + '\n')

    centers = km.cluster_centers_
    weight_matrix = []

    for nr_l, line in enumerate(vectorized_docs): # über alle Chunks iterieren, Distanzen eines jedes Worts zu jedem Center berechnen
        print(nr_l)
        chunk = []
        for center in centers:
            dist = 0
            for word in line:
                dist += np.linalg.norm(center - word)
            chunk.append(dist) # euklidische Distanzen aller Chunks zu allen Clusterzentren errechnen
        weight_matrix.append(chunk)

    weight_array = np.asarray(weight_matrix)
    max = weight_array.max()
    min = weight_array.min()
    weight_matrix = weight_array / max

        #print(chunk)
    print('Größte Distanz: ' + str(max))
    print('Kleinste Distanz: ' + str(min))

   # es wird das finale dic erstellt mit den drei Kategorien "korpus" = alle Interviews; "weight" = Chunk weight Werte; "words" = Wortlisten der Topics
    # vereinfachen möglich! siehe Gespräch mit Dennis

    print("Writing results into top_dic")
    for i in range(len(weight_matrix)):
        #print(weight_matrix[i])
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

    print('Saving metadata')
    # Abspeichern gewisser meta-daten im top_dic
    top_dic["settings"].update({"processed": True})
    top_dic["settings"].update({"model": "w2v"})
    top_dic["settings"].update({"topics": str(topics)})
    top_dic["settings"].update({"coherence": None})
    top_dic["settings"].update({"average_weight": None})
    top_dic["settings"].update({"min_weight": None})
    top_dic["settings"].update({"max_weight": None})

    return top_dic

def topic_modeling_w2v_load_tsne(corpus_dictionary, topics: int=0, chunking: bool=True):
    cores = multiprocessing.cpu_count()  # Count the number of cores in a computer

    w2v_model = Word2Vec(min_count=20,
                     window=2,
                     vector_size=50,
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
                chunk_count = 0
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
            #print(i)
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
    print('Vocab built')

    w2v_model.train(dataset, total_examples=w2v_model.corpus_count, epochs=300, report_delay=1)
    print('Embeddings trained'
          )



    features = [] # Hierarchische Liste, um Chunks aufrechtzuerhalten
    features_avg = [] # Durchschnittswerte für Chunks

    for tokens in dataset:
        #print(tokens)
        zero_vector = np.zeros(w2v_model.vector_size)
        vectors = []
        for token in tokens:
            #print(token)
            if token in w2v_model.wv:
                try:
                    vectors.append(w2v_model.wv[token])
                except KeyError:
                    print('KeyError: ' + str(token))
                    continue
        if vectors:
            features.append(vectors) # jeder Vektor (Wort) eines jeden Chunks in einer Liste
            vectors = np.asarray(vectors) # hier werden die Chunks summiert
            avg_vec = vectors.mean(axis=0) # und ein Mittelwert berechnet
            features_avg.append(avg_vec)
        else:
            features_avg.append(zero_vector)
            features.append([zero_vector])

    vectorized_docs_flat = []

    for chunk in features:
        for feature in chunk:
            vectorized_docs_flat.append(feature)

    vectorized_docs_flat = np.asarray(vectorized_docs_flat)

    vectorized_docs = features

    ## Dimension Reduction
    ## UMAP

    #reducer = umap.UMAP()
    #embedding = reducer.fit_transform(vectorized_docs_flat)


    ##tsne
    embedding = TSNE(n_components=2, learning_rate='auto', init='random', perplexity=30, n_iter=250, verbose=1).fit_transform(vectorized_docs_flat)
    np.save("C:\\Users\\moebusd\\sciebo - Möbus, Dennis (moebusd@fernuni-hagen.de)@fernuni-hagen.sciebo.de\\OHD\\Data TM OHD\\tsne.npy", embedding)
    print(embedding)

    print(len(vectorized_docs))
    print(len(vectorized_docs_flat))
    print(vectorized_docs[:3])
    print(vectorized_docs_flat[:3])

    X = embedding
    k = topics
    mb = 1000
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
    km = MiniBatchKMeans(n_clusters=k, batch_size=mb, verbose=1).fit(X)


    print('Clustering completed, processing output')
    topics_words = []
    embedding_list = embedding.tolist()
    #topics_weights = []
    cluster_centers = km.cluster_centers_.tolist()

    for nr, line in enumerate(cluster_centers):
        print(line)
        #topics_weights.append(str(w2v_model.wv.most_similar(line)))
        topics_words.append(w2v_model.wv.most_similar(vectorized_docs_flat[embedding_list.index(line)], topn=100))
        print(w2v_model.wv.most_similar(vectorized_docs_flat[embedding_list.index(line)], topn=10))

    #for nr, line in enumerate(topics_words):
        #print(str(nr) + " " + str(line) + '\n')
    #for nr, line in enumerate(topics_weights):
    #    print(str(nr) + " " + str(line) + '\n')

    centers = km.cluster_centers_
    weight_matrix = []

    for nr_l, line in enumerate(vectorized_docs): # über alle Chunks iterieren, Distanzen eines jedes Worts zu jedem Center berechnen
        print(nr_l)
        chunk = []
        for center in centers:
            dist = 0
            for word in line:
                dist += np.linalg.norm(center - embedding_list[vectorized_docs_flat.index(word)])
            chunk.append(dist) # euklidische Distanzen aller Chunks zu allen Clusterzentren errechnen
        weight_matrix.append(chunk)

    weight_array = np.asarray(weight_matrix)
    max = weight_array.max()
    min = weight_array.min()
    weight_matrix = weight_array / max

        #print(chunk)
    print('Größte Distanz: ' + str(max))
    print('Kleinste Distanz: ' + str(min))

   # es wird das finale dic erstellt mit den drei Kategorien "korpus" = alle Interviews; "weight" = Chunk weight Werte; "words" = Wortlisten der Topics
    # vereinfachen möglich! siehe Gespräch mit Dennis

    print("Writing results into top_dic")
    for i in range(len(weight_matrix)):
        #print(weight_matrix[i])
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

    print('Saving metadata')
    # Abspeichern gewisser meta-daten im top_dic
    top_dic["settings"].update({"processed": True})
    top_dic["settings"].update({"model": "w2v"})
    top_dic["settings"].update({"topics": str(topics)})
    top_dic["settings"].update({"coherence": None})
    top_dic["settings"].update({"average_weight": None})
    top_dic["settings"].update({"min_weight": None})
    top_dic["settings"].update({"max_weight": None})

    return top_dic

#topic_modeling_w2v(top_dic, topics=75, chunking=True)