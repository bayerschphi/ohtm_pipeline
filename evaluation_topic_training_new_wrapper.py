import mallet_wrapper.corpora as corpora
from mallet_wrapper.ldamallet import LdaMallet
from mallet_wrapper.coherencemodel import CoherenceModel
import json
import copy
import pickle
from datetime import datetime


def evaluation_topic_training_mallet_new(corpus_dictionary, topics, mallet_path,chunk = 10, evaluation_data_1 = "", evaluation_data_2 = "", evaluation_data_3 = "",evaluation_data_4 = "",chunking=True, optimize_interval_mallet: int=500, iterations_mallet:int = 5000, random_seed_mallet: int=100):

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
    coherence_model_ldamallet_1 = CoherenceModel(model=lda_model_mallet,
                                               texts=dataset, dictionary=id2word, coherence='c_v')
    coherence_ldamallet_cv = coherence_model_ldamallet_1.get_coherence()


    coherence_model_ldamallet_2 = CoherenceModel(model=lda_model_mallet,
                                               texts=dataset, dictionary=id2word, coherence='u_mass')

    coherence_model_ldamallet_umass = coherence_model_ldamallet_2.get_coherence()

    coherence_model_ldamallet_3 = CoherenceModel(model=lda_model_mallet,
                                               texts=dataset, dictionary=id2word, coherence='c_uci')

    coherence_model_ldamallet_cuci = coherence_model_ldamallet_3.get_coherence()

    coherence_model_ldamallet_4 = CoherenceModel(model=lda_model_mallet,
                                               texts=dataset, dictionary=id2word, coherence='c_npmi')

    coherence_model_ldamallet_cnpmi = coherence_model_ldamallet_4.get_coherence()



    with open(evaluation_data_1, 'rb') as f:
        evaluation_pipeline_data_1 = pickle.load(f)

    evaluation_pipeline_data_1.append((topics, coherence_ldamallet_cv))

    with open (evaluation_data_1, "wb") as fp:
        pickle.dump(evaluation_pipeline_data_1, fp)

    with open(evaluation_data_2, 'rb') as f:
        evaluation_pipeline_data_2 = pickle.load(f)

    evaluation_pipeline_data_2.append((topics, coherence_model_ldamallet_umass))

    with open (evaluation_data_2, "wb") as fp:
        pickle.dump(evaluation_pipeline_data_2, fp)


    with open(evaluation_data_3, 'rb') as f:
        evaluation_pipeline_data_3 = pickle.load(f)

    evaluation_pipeline_data_3.append((topics, coherence_model_ldamallet_cuci))

    with open (evaluation_data_3, "wb") as fp:
        pickle.dump(evaluation_pipeline_data_3, fp)


    with open(evaluation_data_4, 'rb') as f:
        evaluation_pipeline_data_4 = pickle.load(f)

    evaluation_pipeline_data_4.append((topics, coherence_model_ldamallet_cnpmi))

    with open (evaluation_data_4, "wb") as fp:
        pickle.dump(evaluation_pipeline_data_4, fp)


    print(evaluation_pipeline_data_1)
    print(evaluation_pipeline_data_2)
    print(evaluation_pipeline_data_3)
    print(evaluation_pipeline_data_4)
    print("saving done")

