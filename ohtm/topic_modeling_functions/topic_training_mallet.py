"""
This function calculates the topic model. The mallet_wrapper is based on the gensim wrapper.
The function was deleted in the Version 10. But the developers allowed to copy the wrapper.
See: https://github.com/piskvorky/gensim/releases/tag/4.0.0

Mallet cant handle spaces in patch strings. That's why I set the os.chdri for this patch with the space, if
the model is saved.
"""
from os import environ

import ohtm.mallet_wrapper.corpora as corpora
from ohtm.mallet_wrapper.ldamallet import LdaMallet
from ohtm.mallet_wrapper.coherencemodel import CoherenceModel
import json
import os
from ohtm.basic_functions.convert_ohtm_file import convert_ohtm_file



def topic_training_mallet(ohtm_file, topics, mallet_path,
                          optimize_interval_mallet: int = 500, iterations_mallet: int = 5000,
                          random_seed_mallet: int = 100, alpha: int = 5,
                          save_model: bool = False, working_folder: str = "",
                          save_name: str = "", save_json: bool = False,
                          ):
    if save_model:
        if save_json:
            if not os.path.exists(os.path.join(working_folder, "Models")):
                os.makedirs(os.path.join(working_folder, "Models"))
            if not os.path.exists(os.path.join(working_folder, "Models", save_name)):
                os.makedirs(os.path.join(working_folder, "Models", save_name))
            os.chdir(os.path.join(working_folder, "Models", save_name))
            prefix_value = save_name + "_"
        else:
            print("You need to set a save_name and set the option save_ohtm_file to True to save the model")
            exit()
    else:
        prefix_value = None

    ohtm_file = convert_ohtm_file(ohtm_file)

    # The single sentences are added together to the preprocessed chunks:
    chunk_data = []
    for a in ohtm_file["corpus"]:
        for i in ohtm_file["corpus"][a]:
            chunk_count = 0
            chunk_text = []
            for n in range(1, (len(ohtm_file["corpus"][a][i]["sent"]) + 1)):
                n = str(n)
                if ohtm_file["corpus"][a][i]["sent"][n]["chunk"] == chunk_count:
                    chunk_text += ohtm_file["corpus"][a][i]["sent"][n]["cleaned"]
                    if n == str((len(ohtm_file["corpus"][a][i]["sent"]))):
                        chunk_data += [[a + "%" + i + " chunk*" + str(chunk_count), chunk_text]]
                else:
                    chunk_data += [[a + "%" + i + " chunk*" + str(chunk_count), chunk_text]]
                    chunk_count += 1
                    chunk_text = []
                    chunk_text += ohtm_file["corpus"][a][i]["sent"][n]["cleaned"]
    print(chunk_data[:10])
    dataset = []
    for i in chunk_data:
        dataset += [i[1]]
    print(dataset[:10])
    print("LDA started")
    id2word = corpora.Dictionary(dataset)
    corpus = [id2word.doc2bow(text) for text in dataset]

    lda_model_mallet = LdaMallet(mallet_path=mallet_path,
                                 corpus=corpus,
                                 id2word=id2word,
                                 num_topics=topics,
                                 alpha=alpha,
                                 iterations=iterations_mallet,
                                 optimize_interval=optimize_interval_mallet,
                                 random_seed=random_seed_mallet,
                                 prefix=prefix_value
                                 )

    if save_model:
        lda_model_mallet.save(os.path.join(working_folder, "Models", save_name, (save_name + "_topic_model")))

    # Converting the results and saving them in the dictionary.
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
                if topic_float >= 0:  # Threshold for weight
                    sum_top_weights = sum_top_weights + topic_float
                    top_counter += 1
                    doc_tops_transfer.append((topic_nr - 2, topic_float))
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

    # The results are written in the dictionary.
    for i in range(len(doc_tops_mallet)):
        archive = chunk_data[i][0].split("%")[0]
        interview = chunk_data[i][0].split("%")[1].split(" ")[0]
        interview_chunk = chunk_data[i][0].split("*")[1]
        if archive not in ohtm_file["weight"]:
            ohtm_file["weight"][archive] = {}
        if interview not in ohtm_file["weight"][archive]:
            ohtm_file["weight"][archive][interview] = {}
        if interview_chunk not in ohtm_file["weight"][archive][interview]:
            ohtm_file["weight"][archive][interview][interview_chunk] = {}
        for a in doc_tops_mallet[i]:
            ohtm_file["weight"][archive][interview][interview_chunk][a[0]] = a[1]

    # The results from top_words_mallet for every topic are listed as: (0.000*"zetteln" + 0.000*"sozialisten").
    # We have to split the words at "+" and then split the words from the weight to have a tuple (value, word).

    word_list_splitted = []
    for i in topwords_mallet:
        word_list_splitted += [(i[0], i[1].split("+"))]
    for a in word_list_splitted:
        word_weight_splitted = []
        for b in a[1]:
            c = float(b.split("*")[0])
            d = ((b.split("*")[1]).split('"')[1::2])[0]
            word_weight_splitted += [(c, d)]
        ohtm_file["words"][a[0]] = word_weight_splitted

    for archive in ohtm_file["corpus"]:
        for interviews in ohtm_file["corpus"][archive]:
            ohtm_file["corpus"][archive][interviews]["model_base"] = "trained"

    # Saving metadata and variables.
    ohtm_file["settings"]["topic_modeling"].update({"trained": "True"})
    ohtm_file["settings"]["topic_modeling"].update({"model": "mallet"})
    ohtm_file["settings"]["topic_modeling"].update({"topics": topics})
    ohtm_file["settings"]["topic_modeling"].update({"alpha": alpha})
    ohtm_file["settings"]["topic_modeling"].update({"optimize_interval_mallet": optimize_interval_mallet})
    ohtm_file["settings"]["topic_modeling"].update({"iterations_mallet": iterations_mallet})
    ohtm_file["settings"]["topic_modeling"].update({"random_seed_mallet": random_seed_mallet})
    ohtm_file["settings"]["topic_modeling"].update({"coherence": coherence_ldamallet})
    ohtm_file["settings"]["topic_modeling"].update({"average_weight": average_weight_mallet})
    ohtm_file["settings"]["topic_modeling"].update({"min_weight": min_weight_mallet})
    ohtm_file["settings"]["topic_modeling"].update({"max_weight": max_weight_mallet})

    print("Topic modeling and ohtm_file enrichment finished")

    ohtm_file = json.dumps(ohtm_file, ensure_ascii=False)
    return ohtm_file



