from ohtm_pipeline.ohtm.preprocessing_functions.stopwords import *
from ohtm_pipeline.ohtm.preprocessing_functions.preprocess_outstr import *
from ohtm_pipeline.ohtm.preprocessing_functions.lemmatization import lemmatization

import copy
import json
import spacy


def preprocessing (top_dic, stoplist_path, allowed_postags_settings = ['NOUN', 'PROPN', 'VERB', 'ADJ', 'NUM', 'ADV'],by_list: bool = True, by_particle: bool = True, by_threshold: bool = False, threshold: int=0.5, lemma: bool=True, pos_filter_setting: bool = True):

    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic

    if lemma == True:
        spacy_model = spacy.load('de_core_news_lg', disable=['parser', 'ner'])

    if by_list == True:
        stoplist = open(stoplist_path, encoding='UTF-16', mode='r').read().split()
        stoplist = [word.lower()for word in stoplist]

    sent_length = []
    processed_interviews = 0
    print("Preprocessing started " + str(top_dic["settings"]["interviews"]["total"]) + " interviews")
    for archive in top_dic["corpus"]:
        for interview in top_dic["corpus"][archive]:
            for sent_nr in top_dic["corpus"][archive][interview]["sent"]:
                text = copy.deepcopy(top_dic["corpus"][archive][interview]["sent"][sent_nr]["raw"])
                text = str(text)

                # Text_unified wird zwar auch schon während der dictionary_creation durchgeführt, allerdings nur für die .txt Dateien. Denn dort brauche ich die Satzzeichen zum sauberen Splitten.
                # Die ods und csv raw Texte kann ich ohne die Vereinheitlichung einlesen. Deswegen muss für diese Sätze hier text_unified stattfinden.

                text_unified = text.replace('!', '. ').replace('?', '. ').replace(';', '. ').replace('...,',', ').replace(
                            '..,', ', ').replace('"', ' ').replace("'", ' ').replace("\n", ' ').replace(" - ", " ")
                pre_line = preprocess_outstr(text)
                data_out = pre_line.split(" ") # Tokenisierung
                if lemma == True:
                    goldlist = ["DDR"] # Platzhalter, falls mal eine .txt als goldliste eingesetzt werden soll
                    data_out_lem = lemmatization(data_out, spacy_model, goldlist, pos_filter=pos_filter_setting, allowed_postags=allowed_postags_settings)
                    data_out = data_out_lem
                    top_dic["settings"]["preprocessing"].update({"lemma": "True"})
                    top_dic["settings"]["preprocessing"]["pos_filter"] = pos_filter_setting
                    top_dic["settings"]["preprocessing"]["allowed_postags"] = allowed_postags_settings
                data_out = [word.lower() for word in data_out]
                if by_list == True:
                    top_dic["settings"]["preprocessing"].update({"stopwords_removed": "True"})
                    top_dic["stopwords"] = stoplist
                    data_out = remove_stopwords_by_list(data_out, stoplist)
                if by_particle == True:
                    data_out = remove_particles(data_out)
                    top_dic["settings"]["preprocessing"]["particles_removed"] = "True"
                if by_threshold == True:
                    top_dic["settings"]["preprocessing"].update({"stopwords_removed": "True"})
                    top_dic["settings"]["preprocessing"]["stopword_threshold"] = threshold
                    data_out = remove_stopwords_by_threshold(data_out, threshold)
                data_out = remove_speaker(data_out)
                top_dic["corpus"][archive][interview]["sent"][sent_nr]["cleaned"] = data_out
                sent_length.append(len(data_out))
            processed_interviews += 1
            print(str(processed_interviews) + " out of " + str(top_dic["settings"]["interviews"]["total"]) + " interviews are processed")

    sent_length = [word for word in sent_length if word != 0]
    sent_length.sort()
    max_length = sent_length[-1]
    min_length = sent_length[0]
    average_length = sum(sent_length) / len(sent_length)

    top_dic["settings"]["preprocessing"]["cleaned_length"] = {}
    top_dic["settings"]["preprocessing"]["cleaned_length"]["max_length"] = max_length
    top_dic["settings"]["preprocessing"]["cleaned_length"]["min_length"] = min_length
    top_dic["settings"]["preprocessing"]["cleaned_length"]["ave_length"] = average_length
    top_dic["settings"]["preprocessing"].update({"preprocessed": "True"})



    top_dic = json.dumps(top_dic, ensure_ascii=False)

    return top_dic


