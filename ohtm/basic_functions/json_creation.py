"""
This function converts primary interviews from  .txt .ods and .csv files into the data structure for this topic_modeling
pipeline, called top_dic.
The csv. and .ods files are optimized for the structure of the online archive oral-history.digital.
The txt files are special structured. [ergänzen]

If you only have a plane text, just set speaker_txt to False.
Then each sentence is split by punctuation and will be loaded.

The archive name and the interview id are build from the file name.
The first 3 letters are used as the archive, and the hole name is used as id.

Datastructure:

top_dc:
    corpus:
        archive1
        archive2
            model_base
            sent
                sent_number_1
                sent_number_2
                    raw
                    time
                    tape
                    cleaned
                    speaker
                    chunk
    weight
    words
    settings
        model
        topic_numbuer
"""

import pandas as pd
import os
import re
import json
import csv


def json_creation_function(source: list = "", source_path: str = "", speaker_txt: bool = True):

    # This sections creats the raw dictionary, with the different layers and settings.
    top_dic = {"corpus": {}, "weight": {}, "words": {}, "stopwords": {}, "correlation": {}, "settings": {}}
    top_dic["settings"]["interviews"] = {}
    top_dic["settings"]["interviews"]["total"] = 0
    top_dic["settings"]["interviews_trained"] = {}
    top_dic["settings"]["interviews_inferred"] = {}
    top_dic["settings"]["topic_modeling"] = {}
    top_dic["settings"]["topic_modeling"]["trained"] = "False"
    top_dic["settings"]["topic_modeling"]["inferred"] = "False"
    top_dic["settings"]["preprocessing"] = {}
    top_dic["settings"]["preprocessing"]["preprocessed"] = "False"
    top_dic["settings"]["preprocessing"]["stopwords_removed"] = "False"
    top_dic["settings"]["preprocessing"]["lemma"] = "False"
    top_dic["settings"]["preprocessing"]["chunked"] = "False"
    top_dic["settings"]["preprocessing"]["chunk_setting"] = "None"

    # The documents are loaded from the source_path by creating the path to the folder in the source path.
    # The Iteration loads every single dokument and transforms it into the dictionary.

    for folder in source:   # loads every folder in the source_path folder.
        folder_path = os.path.join(source_path, folder)  # creating the path to the single folders.
        print(folder_path)
        for file in os.listdir(folder_path):  # creats the path and loads the files within the folders.
            print(file)
            file_path = os.path.join(folder_path, file)

            # The code checks, if the file is a .txt, .ods. or .csv file. The different files are processed differently.
            # load the .txt file. For this code, a .txt file with an interview requires a special processing.
            # Especially for masking the speakers. This is shown in the readme.txt
            # If you only have plan text, without a speaker, set the settings of speaker to False.
            if file.split(".")[1] == "txt":
                try:
                    text = open(os.path.join(folder_path, file), 'r', encoding='UTF-8').read()
                except UnicodeDecodeError:
                    try:
                        text = open(file_path, 'r', encoding='UTF-8-sig').read()
                    except UnicodeDecodeError:
                        try:
                            text = open(file_path, 'r', encoding='UTF-16-le').read()
                        except UnicodeDecodeError:
                            try:
                                text = open(file_path, 'r', encoding='UTF-16-be').read()
                            except UnicodeDecodeError:
                                text = open(file_path, 'r', encoding='ANSI').read()
                                text = text.encode('UTF-8')
                                text = text.decode('UTF-8', 'ignore')

                text_unified = (text.replace('!', '. ').replace('?', '. ')
                                .replace(';', '. ')
                                .replace('...,', ', ')
                                .replace('..,', ', ').replace('"', ' ')
                                .replace("'", ' ').replace(" - ", " "))

                text_split = text_unified.split('\n')
                interview_id = file.split(".")[0]
                archive_id = file[:3]
                if archive_id not in top_dic["corpus"]:
                    top_dic["corpus"][archive_id] = {}
                    top_dic["settings"]["interviews"][archive_id] = 0
                top_dic["corpus"][archive_id][interview_id] = {}
                top_dic["settings"]["interviews"][archive_id] = (top_dic["settings"]["interviews"][archive_id])+1
                top_dic["settings"]["interviews"]["total"] = (top_dic["settings"]["interviews"]["total"])+1
                top_dic["corpus"][archive_id][interview_id]["sent"] = {}
                top_dic["corpus"][archive_id][interview_id]["model_base"] = {}
                sent_number = 1
                for line in text_split:
                    if len(line) == 0:  # Skips empty lines in the document.
                        next
                    else:
                        if speaker_txt == True:
                            try:
                                speaker = re.findall(r"^\*(.*?)\*[ ]", line)[0]
                            except IndexError:
                                speaker = speaker

                        text = re.sub(r"<(.*?)>[ ]", "", line)
                        text = re.sub(r"\*(.*?)\*[ ]", "", text)
                        sent_split = text.split(". ")
                        for sent in sent_split:
                            top_dic["corpus"][archive_id][interview_id]["sent"][sent_number] = {}
                            top_dic["corpus"][archive_id][interview_id]["sent"][sent_number]["raw"] = str(sent)
                            top_dic["corpus"][archive_id][interview_id]["sent"][sent_number]["time"] = {}
                            top_dic["corpus"][archive_id][interview_id]["sent"][sent_number]["tape"] = {}
                            top_dic["corpus"][archive_id][interview_id]["sent"][sent_number]["cleaned"] = {}
                            top_dic["corpus"][archive_id][interview_id]["sent"][sent_number]["speaker"] = {}
                            if speaker_txt == True:
                                top_dic["corpus"][archive_id][interview_id]["sent"][sent_number]["speaker"] = str(speaker)
                            top_dic["corpus"][archive_id][interview_id]["sent"][sent_number]["chunk"] = {}
                            sent_number += 1

            # loads the .ods file

            if file.split(".")[1] == "ods":
                interview = pd.read_excel(file_path)
                interview = interview.values.tolist()
                interview_id = file.split(".")[0].split("_")[0]
                if file[:3] not in top_dic["corpus"]:
                    top_dic["corpus"][file[:3]] = {}
                    top_dic["settings"]["interviews"][file[:3]] = 0
                if interview_id not in top_dic["corpus"][file[:3]]:
                    top_dic["corpus"][file[:3]][interview_id] = {}
                    top_dic["settings"]["interviews"][file[:3]] = (top_dic["settings"]["interviews"][file[:3]]) + 1
                    top_dic["settings"]["interviews"]["total"] = (top_dic["settings"]["interviews"]["total"]) + 1
                    top_dic["corpus"][file[:3]][interview_id]["sent"] = {}
                    top_dic["corpus"][file[:3]][interview_id]["model_base"] = {}
                    sent_number = 1
                for line in interview:
                    text = line[2]
                    text = str(text)
                    text_cleaned = re.sub(r"<(.*?)>", " ", text)
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number] = {}
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["raw"] = str(text_cleaned)
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["speaker"] = {}
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["speaker"] = str(line[1])
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["time"] = {}
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["time"] = str(line[0])
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["tape"] = {}
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["tape"] = file.split(".")[0].split("_")[2][1]
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["cleaned"] = {}
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["chunk"] = {}
                    sent_number += 1

            # loads the .csv file. This is the standard type for oral-history.digital.
            # And is the main type for this code.

            if file.split(".")[1] == "csv":
                with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                    interview = csv.reader(csvfile, delimiter="\t", quotechar= None)
                    next(interview) # Skips the first line, the header line of the file.
                    interview_id = file.split(".")[0].split("_")[0]
                    if file[:3] not in top_dic["corpus"]:
                        top_dic["corpus"][file[:3]] = {}
                        top_dic["settings"]["interviews"][file[:3]] = 0
                    if interview_id not in top_dic["corpus"][file[:3]]:
                        top_dic["corpus"][file[:3]][interview_id] = {}
                        top_dic["settings"]["interviews"][file[:3]] = (top_dic["settings"]["interviews"][file[:3]]) + 1
                        top_dic["settings"]["interviews"]["total"] = (top_dic["settings"]["interviews"]["total"]) + 1
                        top_dic["corpus"][file[:3]][interview_id]["sent"] = {}
                        top_dic["corpus"][file[:3]][interview_id]["model_base"] = {}
                        sent_number = 1
                    for line in interview:
                        text = line[3]
                        text2 = str(text)
                        text_cleaned = re.sub(r"<(.*?)>", " ", text2)
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number] = {}
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["raw"] = str(text_cleaned)
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["speaker"] = {}
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["speaker"] = str(line[2])
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["time"] = {}
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["time"] = str(line[1])
                        if str(line[0]) == "":
                            top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["tape"] = "1"
                        else:
                            top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["tape"] = str(line[0])
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["cleaned"] = {}
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["chunk"] = {}
                        sent_number += 1

    top_dic = json.dumps(top_dic, ensure_ascii=False)
    return top_dic
