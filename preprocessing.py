from ohtm.preprocessing_functions.stopwords import *
from ohtm.preprocessing_functions.preprocess_outstr import *
from ohtm.preprocessing_functions.lemmatization import lemmatization_test
import copy
import json
import spacy
import pickle


def preprocessing (top_dic, stoplist_path, bylist: bool = True, byspokenwords: bool = True, bythreshold: bool = False, threshold: int=3, lemmatization: bool=False):
    global goldlist_test
    goldlist_test = []
    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic

    if lemmatization == True:
        spacy_model = spacy.load('de_core_news_lg', disable=['parser', 'ner'])
        goldlist = ['bayrisch']

    if bylist == True:
        stoplist = open(stoplist_path, encoding='UTF-16', mode='r').read().split()

    # Stopwords werden entfernt und unter "cleaned" als Token eingefügt.

    sent_length = []
    processed_interviews = 0
    print("started preprocessing " + str(top_dic["settings"]["interviews"]["total"]) + " interviews")
    for archiv in top_dic["korpus"]:
        for ID in top_dic["korpus"][archiv]:
            for nr in top_dic["korpus"][archiv][ID]["sent"]:
                text = copy.deepcopy(top_dic["korpus"][archiv][ID]["sent"][nr]["raw"])
                text = str(text)
                # text_unified = text.replace('!', '.').replace('?', '.').replace(';', '.').replace('...,',',').replace(
                #             '..,', ',').replace('"', '').replace("'", '').replace("\n", ' ').replace(" - ", " ")
                pre_line = preprocess_outstr(text)
                data_out = pre_line.split(" ") # Tokenisierung
                if lemmatization == True:
                    data_out_lem = lemmatization_test(data_out, spacy_model, goldlist, goldliste_test=goldlist_test, pos_filter = True, allowed_postags=['NOUN', 'PROPN', 'VERB', 'ADJ', 'NUM'])
                    data_out = data_out_lem[0]
                    goldlist_test = data_out_lem[1]
                if bylist == True:
                    data_out = remove_stopwords_by_list(data_out, stoplist)
                if byspokenwords == True:
                    data_out = remove_particles(data_out)
                if bythreshold == True:
                    data_out = remove_stopwords_by_threshold(data_out, threshold)

                top_dic["korpus"][archiv][ID]["sent"][nr]["cleaned"] = data_out
                sent_length.append(len(data_out))
            processed_interviews += 1
            print(str(processed_interviews) + " out of " + str(top_dic["settings"]["interviews"]["total"]) + " interviews are processed")

    sent_length = [word for word in sent_length if word is not 0]
    sent_length.sort()
    max_length = sent_length[-1]
    min_length = sent_length[0]
    average_length = sum(sent_length) / len(sent_length)

    top_dic["settings"]["cleaned_length"] = {}
    top_dic["settings"]["cleaned_length"]["max_length"] = max_length
    top_dic["settings"]["cleaned_length"]["min_length"] = min_length
    top_dic["settings"]["cleaned_length"]["ave_length"] = average_length

    top_dic = json.dumps(top_dic, ensure_ascii=False)

    with open ("C:\\Users\\phili\\FAUbox\\Oral History Digital\\Topic Modeling\\main test\\github_test\\goldlist_test_ZWA_final_test", "wb") as fp:
        pickle.dump(goldlist_test, fp)


    return top_dic


