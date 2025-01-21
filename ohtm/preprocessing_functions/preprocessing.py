"""
This code preprocesses your interviews with the different settings.
    - Tokenization of the sentences into single words
    - lemmatization
    - stopword removal

"""

from ohtm_pipeline.ohtm.preprocessing_functions.stopwords import *
from ohtm_pipeline.ohtm.preprocessing_functions.preprocess_outstr import *
from ohtm_pipeline.ohtm.preprocessing_functions.lemmatization import lemmatization
from ohtm_pipeline.ohtm.basic_functions.convert_ohtm_file import convert_ohtm_file
import copy
import json
import spacy


def preprocessing(ohtm_file, stoplist_path: str = "",
                  allowed_postags_settings=None,
                  by_list: bool = False, by_particle: bool = False, by_threshold: bool = False, threshold: int = 0.5,
                  lemma: bool = False, pos_filter_setting: bool = False, stop_words: list = "",
                  infer_new_documents: bool = False, spacy_model: str = ""
                  ):

    if allowed_postags_settings is None:
        allowed_postags_settings = ['NOUN', 'PROPN', 'VERB', 'ADJ', 'NUM', 'ADV']

    ohtm_file = convert_ohtm_file(ohtm_file)

    if lemma:
        spacy_model = spacy.load(spacy_model, disable=['parser', 'ner'])

    if by_list:
        if infer_new_documents:
            stoplist = stop_words
        else:
            stoplist = open(stoplist_path, encoding='UTF-16', mode='r').read().split()
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
                if lemma:
                    goldlist = [""]  # Placeholder for a goldlist, to exclude words from filtering.
                    data_out_lem = lemmatization(data_out,
                                                 spacy_model,
                                                 goldlist,
                                                 pos_filter=pos_filter_setting,
                                                 allowed_postags=allowed_postags_settings)
                    data_out = data_out_lem
                    ohtm_file["settings"]["preprocessing"].update({"lemma": "True"})
                    ohtm_file["settings"]["preprocessing"]["pos_filter"] = pos_filter_setting
                    ohtm_file["settings"]["preprocessing"]["allowed_postags"] = allowed_postags_settings
                data_out = [word.lower() for word in data_out]

                if by_list:
                    ohtm_file["settings"]["preprocessing"].update({"stopwords_removed": "True"})
                    ohtm_file["stopwords"] = stoplist
                    data_out = remove_stopwords_by_list(data_out, stoplist)

                if by_particle:
                    data_out = remove_particles(data_out)
                    ohtm_file["settings"]["preprocessing"]["particles_removed"] = "True"

                if by_threshold:
                    ohtm_file["settings"]["preprocessing"].update({"stopwords_removed": "True"})
                    ohtm_file["settings"]["preprocessing"]["stopword_threshold"] = threshold
                    data_out = remove_stopwords_by_threshold(data_out, threshold)
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
    ohtm_file["settings"]["preprocessing"]["by_list"] = by_list
    ohtm_file["settings"]["preprocessing"]["by_particle"] = by_particle
    ohtm_file["settings"]["preprocessing"]["by_threshold"] = by_threshold
    ohtm_file["settings"]["preprocessing"]["threshold_stopwords"] = threshold
    ohtm_file["settings"]["preprocessing"]["lemmatization"] = lemma
    ohtm_file["settings"]["preprocessing"]["pos_filter_setting"] = pos_filter_setting
    ohtm_file["settings"]["preprocessing"].update({"preprocessed": "True"})

    ohtm_file = json.dumps(ohtm_file, ensure_ascii=False)

    return ohtm_file


