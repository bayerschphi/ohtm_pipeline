"""
This code preprocesses your interviews with the different settings.
    - Tokenization of the sentences into single words
    - lemmatization
    - stopword removal

"""

from ohtm.preprocessing_functions.stopwords import (remove_stopwords_by_list,
                                                remove_particles, remove_stopwords_by_threshold)
from ohtm.preprocessing_functions.preprocess_outstr import preprocess_outstr
from ohtm.preprocessing_functions.lemmatization import lemmatization
from ohtm.basic_functions.convert_ohtm_file import convert_ohtm_file
import copy
import json
import spacy
import os


def preprocessing(ohtm_file, stoplist_name: str = "",
                  allowed_postags_settings=None,
                  by_list: bool = False, by_particle: bool = False, by_threshold: bool = False, threshold: int = 0.5,
                  lemma: bool = False, pos_filter_setting: bool = False, stop_words: list = "",
                  infer_new_documents: bool = False, spacy_model: str = "", stopword_removal_by_spacy: bool = False,
                  working_folder: str = ""
                  ):

    if allowed_postags_settings is None:
        allowed_postags_settings = ['NOUN', 'PROPN', 'VERB', 'ADJ', 'NUM', 'ADV']

    ohtm_file = convert_ohtm_file(ohtm_file)

    if lemma:
        try:
            spacy_model_load = spacy.load(spacy_model, disable=['parser', 'ner'])
        except ValueError:
            print("You need a spacy model name")
            exit()
        except OSError:
            print("Your spacy model name is not correct")
            exit()
    if stopword_removal_by_spacy:
        try:
            spacy_model_load = spacy.load(spacy_model, disable=['parser', 'ner'])
            stop_list_spacy = spacy_model_load.Defaults.stop_words
        except ValueError:
            print("You need a spacy model name")
            exit()
        except OSError:
            print("Your spacy model name is not correct")
            exit()
    if by_particle:
        print("Stopwords removal by particle is not included so far")
    if by_list:
        if infer_new_documents:
            stoplist = stop_words
        else:
            stoplist = open(os.path.join(working_folder, stoplist_name), encoding='UTF-16', mode='r').read().split()
        stoplist = [word.lower()for word in stoplist]

    sent_length = []
    processed_interviews = 0
    print("Preprocessing started " + str(ohtm_file["settings"]["interviews"]["total"]) + " interviews")
    for archive in ohtm_file["corpus"]:
        for interview in ohtm_file["corpus"][archive]:
            for sent_nr in ohtm_file["corpus"][archive][interview]["sent"]:
                text = copy.deepcopy(ohtm_file["corpus"][archive][interview]["sent"][sent_nr]["raw"])
                text = str(text)
                pre_line = preprocess_outstr(text)
                data_out = pre_line.split(" ")  # Tokenization
                data_out = [word.lower() for word in data_out]
                if by_list:
                    ohtm_file["settings"]["preprocessing"].update({"stopwords_removed": "True"})
                    ohtm_file["stopwords"] = stoplist
                    data_out = remove_stopwords_by_list(data_out, stoplist)
                if by_particle:
                    # data_out = remove_particles(data_out)
                    ohtm_file["settings"]["preprocessing"]["particles_removed"] = "False"
                if by_threshold:
                    ohtm_file["settings"]["preprocessing"].update({"stopwords_removed": "True"})
                    ohtm_file["settings"]["preprocessing"]["stopword_threshold"] = threshold
                    data_out = remove_stopwords_by_threshold(data_out, threshold)
                if stopword_removal_by_spacy:
                    data_out = [word for word in data_out if word.lower() not in stop_list_spacy]
                    stop_list = [word for word in stop_list_spacy]
                    ohtm_file["stopwords"] = stop_list

                if lemma:
                    goldlist = [""]  # Placeholder for a goldlist, to exclude words from filtering.
                    data_out_lem = lemmatization(data_out,
                                                 spacy_model_load,
                                                 goldlist,
                                                 pos_filter=pos_filter_setting,
                                                 allowed_postags=allowed_postags_settings)
                    data_out = data_out_lem
                    ohtm_file["settings"]["preprocessing"].update({"lemma": "True"})
                    ohtm_file["settings"]["preprocessing"]["pos_filter"] = pos_filter_setting
                    ohtm_file["settings"]["preprocessing"]["allowed_postags"] = allowed_postags_settings
                else:
                    ohtm_file["settings"]["preprocessing"]["pos_filter"] = False
                    ohtm_file["settings"]["preprocessing"]["allowed_postags"] = []

                data_out = remove_speaker(data_out)
                ohtm_file["corpus"][archive][interview]["sent"][sent_nr]["cleaned"] = data_out
                sent_length.append(len(data_out))
            processed_interviews += 1
            print(str(processed_interviews) + " out of " + str(ohtm_file["settings"]["interviews"]["total"]) +
                  " interviews are processed")

    sent_length = [word for word in sent_length if word != 0]
    sent_length.sort()
    max_length = sent_length[-1]
    min_length = sent_length[0]
    average_length = sum(sent_length) / len(sent_length)

    # Saves the settings in the dictionary.
    ohtm_file["settings"]["preprocessing"]["cleaned_length"] = {}
    ohtm_file["settings"]["preprocessing"]["cleaned_length"]["max_length"] = max_length
    ohtm_file["settings"]["preprocessing"]["cleaned_length"]["min_length"] = min_length
    ohtm_file["settings"]["preprocessing"]["cleaned_length"]["ave_length"] = average_length
    ohtm_file["settings"]["preprocessing"]["stopwords_by_list"] = by_list
    ohtm_file["settings"]["preprocessing"]["stop_words_by_particle"] = by_particle
    ohtm_file["settings"]["preprocessing"]["stop_words_by_threshold"] = by_threshold
    ohtm_file["settings"]["preprocessing"]["stop_words_by_spacy"] = stopword_removal_by_spacy
    ohtm_file["settings"]["preprocessing"]["stop_words_by_threshold"] = threshold
    ohtm_file["settings"]["preprocessing"]["lemmatization"] = lemma
    ohtm_file["settings"]["preprocessing"]["pos_filter_setting"] = pos_filter_setting
    ohtm_file["settings"]["preprocessing"].update({"preprocessed": "True"})

    ohtm_file = json.dumps(ohtm_file, ensure_ascii=False)

    return ohtm_file


