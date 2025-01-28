"""

"""
from ohtm.mallet_wrapper.ldamallet import LdaMallet
import json
import os
from ohtm.basic_functions.convert_ohtm_file import convert_ohtm_file


def topic_inferring(ohtm_file,
                    mallet_path: str = "", model_name: str = "", working_folder: str = "",
                    topics: int = 0, iterations_mallet: int = 5000, random_seed_mallet: int = 100):

    # Load the train model and set all necessary variables.
    model_path = os.path.join(working_folder, "Models", model_name, model_name+"_")
    lda_model_mallet = LdaMallet.load(model_path+"topic_model")
    os.chdir(os.path.join(working_folder, "Models", model_name))
    lda_model_mallet.prefix = model_name + "_"
    lda_model_mallet.random_seed = random_seed_mallet

    # The single sentences are added together to the preprocessed chunks:
    ohtm_file = convert_ohtm_file(ohtm_file)

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
                        chunk_data += [[a + "%" + i + " chunk_" + str(chunk_count), chunk_text]]
                else:
                    chunk_data += [[a + "%" + i + " chunk_" + str(chunk_count), chunk_text]]
                    chunk_count += 1
                    chunk_text = []
                    chunk_text += ohtm_file["corpus"][a][i]["sent"][n]["cleaned"]

    dataset = []
    for i in chunk_data:
        dataset += [i[1]]

    print("Starting inferring")

    corpus = [lda_model_mallet.id2word.doc2bow(text) for text in dataset]
    lda_model_mallet[corpus]
    # Converting the results and saving them in the dictionary.
    doc_tops_import = open(lda_model_mallet.fdoctopics() + ".infer", mode='r', encoding='UTF-8').read()

    doc_tops_mallet = []
    sum_top_weights = 0.0
    top_counter = 0
    min_weight_mallet = 1
    max_weight_mallet = 0
    for line in doc_tops_import.splitlines():
        if line.startswith("#doc"):  # The .infer doc has a headline that starts with #doc and has to be skipped
            continue
        doc_tops_transfer = []
        for topic_nr, topic in enumerate(line.split()):
            if '.' in topic:
                topic_float = float(topic)
                if topic_float >= 0:  # Threshold für Weight
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

    # The results are written in the dictionary.
    for i in range(len(doc_tops_mallet)):
        archive = chunk_data[i][0].split("%")[0]
        interview = chunk_data[i][0].split("%")[1].split(" ")[0]
        interview_chunk = chunk_data[i][0].split("_")[1]
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
            ohtm_file["corpus"][archive][interviews]["model_base"] = "inferred"

    # Saving metadata and variables.
    ohtm_file["settings"]["topic_modeling"]["inferred"] = "True"
    ohtm_file["settings"]["topic_modeling"]["trained"] = "True"
    ohtm_file["settings"]["topic_inferred"] = {}
    ohtm_file["settings"]["topic_inferred"]["infer_model"] = model_name
    ohtm_file["settings"]["topic_inferred"].update({"model": "mallet"})
    ohtm_file["settings"]["topic_inferred"].update({"topics": topics})
    ohtm_file["settings"]["topic_inferred"].update({"iterations_mallet": iterations_mallet})
    ohtm_file["settings"]["topic_inferred"].update({"average_weight": average_weight_mallet})
    ohtm_file["settings"]["topic_inferred"].update({"min_weight": min_weight_mallet})
    ohtm_file["settings"]["topic_inferred"].update({"max_weight": max_weight_mallet})

    ohtm_file = json.dumps(ohtm_file, ensure_ascii=False)
    return ohtm_file



