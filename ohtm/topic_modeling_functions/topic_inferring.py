import mallet_wrapper.corpora as corpora
from mallet_wrapper.ldamallet import LdaMallet
from mallet_wrapper.coherencemodel import CoherenceModel
import json
import os
from mallet_wrapper.utils import SaveLoad

def topic_inferring(corpus_dictionary, mallet_path:str ="", model_name: str = "", working_folder: str ="", topics: int = 0, iterations_mallet:int = 5000, random_seed_mallet: int=100):

    # Load the train model and set all necessary variables.
    model_path = os.path.join(working_folder, "Models", model_name, model_name+"_")
    lda_model_mallet = LdaMallet.load(model_path+"topic_model")

    lda_model_mallet.prefix = model_path
    lda_model_mallet.random_seed = random_seed_mallet



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

    print("Starting inferring")

    corpus = [lda_model_mallet.id2word.doc2bow(text) for text in dataset]

    lda_model_mallet[corpus]


    ## Daten-Output Mallet konvertieren

    doc_tops_import = open(lda_model_mallet.fdoctopics() + ".infer", mode='r', encoding='UTF-8').read()

    doc_tops_mallet = []
    sum_top_weights = 0.0
    top_counter = 0
    min_weight_mallet = 1
    max_weight_mallet = 0
    for line in doc_tops_import.splitlines():
        if line.startswith("#doc"): # The .infer doc has a headline that starts with #doc and has to be skipped
            continue
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


    for archive in top_dic["corpus"]:
        for interviews in top_dic["corpus"][archive]:
            top_dic["corpus"][archive][interviews]["model_base"] = "inferred"


    # Abspeichern gewisser meta-daten im top_dic
    top_dic["settings"]["topic_modeling"]["inferred"] = "True"
    top_dic["settings"]["topic_modeling"]["trained"] = "True"
    top_dic["settings"]["topic_inferred"]= {}
    top_dic["settings"]["topic_inferred"]["infer_model"] = model_name
    top_dic["settings"]["topic_inferred"].update({"model": "mallet"})
    top_dic["settings"]["topic_inferred"].update({"topics": topics})
    top_dic["settings"]["topic_inferred"].update({"iterations_mallet": iterations_mallet})
    top_dic["settings"]["topic_inferred"].update({"average_weight": average_weight_mallet})
    top_dic["settings"]["topic_inferred"].update({"min_weight": min_weight_mallet})
    top_dic["settings"]["topic_inferred"].update({"max_weight": max_weight_mallet})


    top_dic = json.dumps(top_dic, ensure_ascii=False)
    return top_dic



