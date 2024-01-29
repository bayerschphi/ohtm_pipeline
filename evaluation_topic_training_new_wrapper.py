import mallet_wrapper.corpora as corpora
from mallet_wrapper.ldamallet import LdaMallet
from mallet_wrapper.coherencemodel import CoherenceModel
import json
import copy
import pickle
from datetime import datetime


def evaluation_topic_training_mallet_new(corpus_dictionary, topics, mallet_path,chunk = 10, evaluation_data = "", chunking=True, optimize_interval_mallet: int=500, iterations_mallet:int = 5000, random_seed_mallet: int=100):

    # Aus dem top_dic werden die einzelenen Tokens Listen ausgelesen.

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


    id2word = corpora.Dictionary(dataset)
    corpus = [id2word.doc2bow(text) for text in dataset]

    lda_model_mallet = LdaMallet(mallet_path, corpus=corpus, id2word=id2word,
                                                                  num_topics=topics, iterations=iterations_mallet,
                                                                  optimize_interval=optimize_interval_mallet,
                                                                  random_seed=random_seed_mallet)

    print("LDA done")
    coherence_model_ldamallet = CoherenceModel(model=lda_model_mallet,
                                               texts=dataset, dictionary=id2word, coherence='c_v')
    coherence_ldamallet = coherence_model_ldamallet.get_coherence()

    print(coherence_ldamallet)

    # with open('evaluation_data', 'rb') as f:
    #     evluation_pipeline_data = pickle.load(f)

    evaluation_pipeline_data = []
    evaluation_pipeline_data.append((topics, coherence_ldamallet))

    with open (evaluation_data, "wb") as fp:
        pickle.dump(evaluation_pipeline_data, fp)


    test = open(str(topics) +"_" + str(chunk), "wb")
    pickle.dump(coherence_ldamallet, test)
    print("saving done")

