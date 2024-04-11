import mallet_wrapper.corpora as corpora
from mallet_wrapper.ldamallet import LdaMallet
from mallet_wrapper.coherencemodel import CoherenceModel
import gensim
import json
from datetime import datetime


def topic_training_mallet(corpus_dictionary, topics, mallet_path, optimize_interval_mallet: int=500, iterations_mallet:int = 5000, random_seed_mallet: int=100, alpha: int=5):

    # Aus dem top_dic werden die einzelenen Tokens Listen ausgelesen.

    if type(corpus_dictionary) is not dict:
        top_dic = json.loads(corpus_dictionary)
    else:
        top_dic = corpus_dictionary



    chunk_data = []
    for a in top_dic["corpus"]:
        for i in top_dic["corpus"][a]:
            chunk_count = 0
            chunk_text = []
            for n in range(1, (len(top_dic["corpus"][a][i]["sent"]) + 1)):
                n = str(n)
                if top_dic["corpus"][a][i]["sent"][n]["chunk"] == chunk_count:
                    chunk_text += top_dic["corpus"][a][i]["sent"][n]["cleaned"]
                    if n == str((len(top_dic["corpus"][a][i]["sent"]))):
                        chunk_data += [[i + " chunk_" + str(chunk_count), chunk_text]]

                else:
                    chunk_data += [[i + " chunk_" + str(chunk_count), chunk_text]]
                    chunk_count += 1
                    chunk_text = []
                    chunk_text += top_dic["corpus"][a][i]["sent"][n]["cleaned"]
    dataset = []
    for i in chunk_data:
        dataset += [i[1]]


    id2word = corpora.Dictionary(dataset)
    corpus = [id2word.doc2bow(text) for text in dataset]

    lda_model_mallet = LdaMallet(mallet_path, corpus=corpus, id2word=id2word,
                                                                  num_topics=topics, alpha = alpha, iterations=iterations_mallet,
                                                                  optimize_interval=optimize_interval_mallet,
                                                                  random_seed=random_seed_mallet)




    ## Daten-Output Mallet konvertieren

    doc_tops_import = open(lda_model_mallet.fdoctopics(), mode='r', encoding='UTF-8').read()

    doc_tops_mallet = []
    sum_top_weights = 0.0
    top_counter = 0
    min_weight_mallet = 1
    max_weight_mallet = 0
    for line in doc_tops_import.splitlines():
        doc_tops_transfer = []
        for topic_nr, topic in enumerate(line.split()):
            if '.' in topic:
                topic_float = float(topic)
                if topic_float >= 0:  # Threshold für Weight
                    sum_top_weights = sum_top_weights + topic_float
                    top_counter += 1
                    doc_tops_transfer.append((topic_nr - 2,
                                              topic_float))  # hier Weight als Float, in anderen Zellen als Str -> vereinheitlichen (?)
                    if topic_float < min_weight_mallet:
                        min_weight_mallet = topic_float
                    if topic_float > max_weight_mallet:
                        max_weight_mallet = topic_float
        doc_tops_mallet.append(doc_tops_transfer)

    average_weight_mallet = sum_top_weights / top_counter

    topwords_mallet = lda_model_mallet.print_topics(num_topics=topics, num_words=1000)

    coherence_model_ldamallet = CoherenceModel(model=lda_model_mallet,
                                               texts=dataset, dictionary=id2word, coherence='c_v')
    coherence_ldamallet = coherence_model_ldamallet.get_coherence()




    # es wird das finale dic erstellt mit den drei Kategorien "corpus" = alle Interviews; "weight" = Chunk weight Werte; "words" = Wortlisten der Topics
    # vereinfachen möglich! siehe Gespräch mit Dennis



    for i in range(len(doc_tops_mallet)):
        if chunk_data[i][0].split(" ")[0][:3] not in top_dic["weight"]:
            top_dic["weight"][chunk_data[i][0].split(" ")[0][:3]] = {}
        if chunk_data[i][0].split(" ")[0] not in top_dic["weight"][chunk_data[i][0].split(" ")[0][:3]]:
            top_dic["weight"][chunk_data[i][0].split(" ")[0][:3]][chunk_data[i][0].split(" ")[0]] = {}
        if chunk_data[i][0].split("_")[1] not in top_dic["weight"][chunk_data[i][0].split(" ")[0][:3]][
            chunk_data[i][0].split(" ")[0]]:
            top_dic["weight"][chunk_data[i][0].split(" ")[0][:3]][chunk_data[i][0].split(" ")[0]][
                chunk_data[i][0].split("_")[1]] = {}
        for a in doc_tops_mallet[i]:
            top_dic["weight"][chunk_data[i][0].split(" ")[0][:3]][chunk_data[i][0].split(" ")[0]][
                chunk_data[i][0].split("_")[1]][a[0]] = a[1]


    # Zuerst werden die Ergebnislisten aus top_words_mallet getrennt, da sie in einer Kette mit "+" aneinandergedliedert sind. (0.000*"zetteln" + 0.000*"salonsozialisten") und an word_list_splittet übergeben
    # anschließend wird das Wort*Wert geflecht getrennt und als Tupel (Wert, Wort) passend zu seinem Topic dem dic übergeben.


    word_list_splitted = []
    for i in topwords_mallet:
        word_list_splitted += [(i[0], i[1].split("+"))]
    for a in word_list_splitted:
        word_weight_splitted = []
        for b in a[1]:
            c = float(b.split("*")[0])
            d = ((b.split("*")[1]).split('"')[1::2])[0]
            word_weight_splitted += [(c, d)]
        top_dic["words"][a[0]] = word_weight_splitted


    # Abspeichern gewisser meta-daten im top_dic
    top_dic["settings"]["topic_modeling"].update({"trained":"True"})
    top_dic["settings"]["topic_modeling"].update({"model": "mallet"})
    top_dic["settings"]["topic_modeling"].update({"topics": topics})
    top_dic["settings"]["topic_modeling"].update({"alpha": alpha})
    top_dic["settings"]["topic_modeling"].update({"optimize_interval_mallet": optimize_interval_mallet})
    top_dic["settings"]["topic_modeling"].update({"iterations_mallet": iterations_mallet})
    top_dic["settings"]["topic_modeling"].update({"coherence": coherence_ldamallet})
    top_dic["settings"]["topic_modeling"].update({"average_weight": average_weight_mallet})
    top_dic["settings"]["topic_modeling"].update({"min_weight": min_weight_mallet})
    top_dic["settings"]["topic_modeling"].update({"max_weight": max_weight_mallet})



    print('\nCoherence Score: ', coherence_ldamallet)

    print('Minimales Topic-Weight Mallet: ' + str(min_weight_mallet))
    print('Durchschnittliches Topic-Weight Mallet: ' + str(average_weight_mallet))
    print('Maximales Topic-Weight Mallet: ' + str(max_weight_mallet))

    top_dic = json.dumps(top_dic, ensure_ascii=False)
    return top_dic



