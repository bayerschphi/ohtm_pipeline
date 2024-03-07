import json
import multiprocessing
from scipy.spatial import distance
import numpy as np
from gensim.models import Word2Vec

def topic_consistency(top_dic, corpus_vectorized):
    nr_topwords = 10
    topics = []
    for topic in top_dic["words"]:
        topic_transfer = [topic, []]
        for word in top_dic["words"][topic][:nr_topwords]:
            topic_transfer[1].append(word[1])
        topics.append(topic_transfer)

    w2v_model = Word2Vec.load(corpus_vectorized) # erstellen einer Liste mit den Wörtern oder Vektoren der TopWords
    topic_vectors = []
    for topic in topics:
        topic_transfer = []
        for word in topic[1]:
            topic_transfer.append(word)#(w2v_model.wv[word]) #hier auf Vektoren wechseln
        topic_vectors.append(topic_transfer)

    topic_vectors_array = np.asarray(topic_vectors)

    top_dists = []

    for i, line in enumerate(topic_vectors_array):
        print("Topic"+str(i))
        sum_weight = 0
        for id, word1 in enumerate(line):
            for word2 in line[id+1:]:
                sum_weight += w2v_model.wv.similarity(word1, word2)
                print(word1, word2, str(w2v_model.wv.similarity(word1, word2)))
        top_dists.append(sum_weight/(((nr_topwords*nr_topwords)-nr_topwords)/2))



        #print(line)                            # Referenzpunkt ist erstes Wort im Topic
        #reference_word = line[0]
        #for word in line[1:]:
        #    print(reference_word, word, str(w2v_model.wv.similarity(word, reference_word)))
        #top_dists.append(sum(w2v_model.wv.similarity(word, reference_word) for word in line[1:]))
        #print(sum(distance.cosine(word, reference_word) for word in line))
    for line in top_dists:
        print(line)





def corpus_vectorized(top_dic, destination, chunking: bool=True):

    cores = multiprocessing.cpu_count()  # Count the number of cores in a computer

    w2v_model = Word2Vec(min_count=20,
                     window=2,
                     vector_size=10,
                     sample=6e-5,
                     alpha=0.03,
                     min_alpha=0.0007,
                     negative=20,
                     workers=cores-1)

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

    w2v_model.train(dataset, total_examples=w2v_model.corpus_count, epochs=100, report_delay=1)
    print('Embeddings trained'
          )
    w2v_model.save(destination)


load_file_name = "OHD_complete_29_01_2024_pre_100C_100T"
working_folder = "C:\\Users\\moebusd\\sciebo - Möbus, Dennis (moebusd@fernuni-hagen.de)@fernuni-hagen.sciebo.de\\OHD\\Data TM OHD\\"

with open(working_folder + load_file_name) as f:
    top_dic = json.load(f)


path = "C:\\Users\\moebusd\\sciebo - Möbus, Dennis (moebusd@fernuni-hagen.de)@fernuni-hagen.sciebo.de\\OHD\\Data TM OHD\\"
#corpus_vectorized(top_dic, path+"w2v 10dims.model", chunking=True)
topic_consistency(top_dic, path+"w2v 300dims.model")