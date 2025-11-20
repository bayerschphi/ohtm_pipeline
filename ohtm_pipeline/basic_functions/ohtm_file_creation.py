"""
This function converts primary interviews from  .txt .ods and .csv files into the data structure for this topic_modeling
pipeline, called top_dic.
The csv. and .ods files are optimized for the structure of the online archive oral-history.digital.
The txt files are special structured. [ergänzen]

If you only have a plane text, just set speaker_txt to False.
Then each sentence is split by punctuation and will be loaded.

The archive name and the interview id are build from the file name.
The first 3 letters are used as the archive, and the hole name is used as id.
"""

import pandas as pd
import os
import re
import json
import csv


def ohtm_file_creation_function(source: list = "", source_path: str = "",
                                speaker_txt: bool = True, folder_as_archive: bool = False):

    # This sections creats the raw dictionary, with the different layers and settings.
    ohtm_file = {"corpus": {}, "weight": {}, "words": {}, "stopwords": {}, "correlation": {}, "settings": {}}
    ohtm_file["settings"]["interviews"] = {}
    ohtm_file["settings"]["interviews"]["total"] = 0
    ohtm_file["settings"]["interviews_trained"] = {}
    ohtm_file["settings"]["interviews_inferred"] = {}
    ohtm_file["settings"]["topic_modeling"] = {}
    ohtm_file["settings"]["topic_modeling"]["trained"] = "False"
    ohtm_file["settings"]["topic_modeling"]["inferred"] = "False"
    ohtm_file["settings"]["preprocessing"] = {}
    ohtm_file["settings"]["preprocessing"]["preprocessed"] = "False"
    ohtm_file["settings"]["preprocessing"]["stopwords_removed"] = "False"
    ohtm_file["settings"]["preprocessing"]["lemma"] = "False"
    ohtm_file["settings"]["preprocessing"]["chunked"] = "False"
    ohtm_file["settings"]["preprocessing"]["chunk_setting"] = "None"
    ohtm_file["settings"]["anonymized"] = {}
    ohtm_file["settings"]["anonymized"]["anonymized"] = "False"
    ohtm_file["settings"]["anonymized"]["exceptions"] = ()
    ohtm_file["settings"]["ohtm_file_version"] = 0.8

    # The documents are loaded from the source_path by creating the path to the folder in the source path.
    # The Iteration loads every single dokument and transforms it into the dictionary.

    for folder in source:   # loads every folder in the source_path folder.
        archive_id_name_folder = (str(folder)).lower()
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
                        text = open(os.path.join(folder_path, file), 'r', encoding='UTF-8-sig').read()
                    except UnicodeDecodeError:
                        try:
                            text = open(os.path.join(folder_path, file), 'r', encoding='UTF-16-le').read()
                        except UnicodeDecodeError:
                            try:
                                text = open(os.path.join(folder_path, file), 'r', encoding='UTF-16-be').read()
                            except UnicodeDecodeError:
                                text = open(os.path.join(folder_path, file), 'r', encoding='ANSI').read()
                                text = text.encode('UTF-8')
                                text = text.decode('UTF-8', 'ignore')

                text_unified = (text.replace('!', '. ').replace('?', '. ').replace(
                    ';', '. ').replace(
                    '...,', ', ').replace(
                    '..,', ', ').replace('"', ' ').replace(
                    "'", ' ').replace(" - ", " "))

                text_split = text_unified.split('\n')
                interview_id = file.split(".")[0].lower()
                if folder_as_archive:
                    archive_id = archive_id_name_folder
                else:
                    archive_id = file[:3].lower()
                if archive_id not in ohtm_file["corpus"]:
                    ohtm_file["corpus"][archive_id] = {}
                    ohtm_file["settings"]["interviews"][archive_id] = 0
                ohtm_file["corpus"][archive_id][interview_id] = {}
                ohtm_file["settings"]["interviews"][archive_id] = (ohtm_file["settings"]["interviews"][archive_id])+1
                ohtm_file["settings"]["interviews"]["total"] = (ohtm_file["settings"]["interviews"]["total"])+1
                ohtm_file["corpus"][archive_id][interview_id]["sent"] = {}
                ohtm_file["corpus"][archive_id][interview_id]["model_base"] = {}
                ohtm_file["corpus"][archive_id][interview_id]["anonymized"] = False
                sent_number = 1
                for line in text_split:
                    if len(line) == 1:
                        print("line is zero")
                    else:
                        if speaker_txt:
                            try:
                                line = line.lstrip('\ufeff')
                                speaker = re.findall(r"^\*(.*?)\*[ ]", line)[0]
                            except IndexError:
                                speaker = speaker
                        text = re.sub(r"<(.*?)>[ ]", "", line)
                        text = re.sub(r"\*(.*?)\*[ ]", "", text)
                        sent_split = text.split(". ")
                        for sent in sent_split:
                            ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number] = {}
                            ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["raw"] = str(sent)
                            ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["time"] = {}
                            ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["tape"] = {}
                            ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["cleaned"] = {}
                            ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["speaker"] = {}
                            if speaker_txt:
                                ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["speaker"]\
                                    = str(speaker)
                            ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["chunk"] = {}
                            sent_number += 1

            # loads the .ods file

            if file.split(".")[1] == "ods":
                interview = pd.read_excel(file_path)
                if folder_as_archive:
                    archive_id = archive_id_name_folder
                else:
                    archive_id = (file[:3]).lower()
                interview = interview.values.tolist()
                interview_id = (file.split(".")[0].split("_")[0]).lower()
                if archive_id not in ohtm_file["corpus"]:
                    ohtm_file["corpus"][archive_id] = {}
                    ohtm_file["settings"]["interviews"][archive_id] = 0
                if interview_id not in ohtm_file["corpus"][archive_id]:
                    ohtm_file["corpus"][archive_id][interview_id] = {}
                    ohtm_file["settings"]["interviews"][archive_id] = (ohtm_file["settings"]["interviews"][archive_id]) + 1
                    ohtm_file["settings"]["interviews"]["total"] = (ohtm_file["settings"]["interviews"]["total"]) + 1
                    ohtm_file["corpus"][archive_id][interview_id]["sent"] = {}
                    ohtm_file["corpus"][archive_id][interview_id]["model_base"] = {}
                    sent_number = 1
                for line in interview:
                    text = line[2]
                    text = str(text)
                    text_cleaned = re.sub(r"<(.*?)>", " ", text)
                    ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number] = {}
                    ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["raw"] = str(text_cleaned)
                    ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["speaker"] = {}
                    ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["speaker"] = str(line[1])
                    ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["time"] = {}
                    ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["time"] = str(line[0])
                    ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["tape"] = {}
                    ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["tape"] = file.split(".")[0].split("_")[2][1]
                    ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["cleaned"] = {}
                    ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["chunk"] = {}
                    sent_number += 1

            # loads the .csv file. This is the standard type for oral-history.digital.
            # And is the main type for this code.

            if file.split(".")[1] == "csv":
                with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                    interview = csv.reader(csvfile, delimiter="\t", quotechar= None)
                    next(interview) # Skips the first line, the header line of the file.
                    interview_id = (file.split(".")[0].split("_")[0]).lower()
                    if folder_as_archive:
                        archive_id = archive_id_name_folder
                    else:
                        archive_id = (file[:3]).lower()
                    if archive_id not in ohtm_file["corpus"]:
                        ohtm_file["corpus"][archive_id] = {}
                        ohtm_file["settings"]["interviews"][archive_id] = 0
                    if interview_id not in ohtm_file["corpus"][archive_id]:
                        ohtm_file["corpus"][archive_id][interview_id] = {}
                        ohtm_file["settings"]["interviews"][archive_id] = (ohtm_file["settings"]["interviews"][archive_id]) + 1
                        ohtm_file["settings"]["interviews"]["total"] = (ohtm_file["settings"]["interviews"]["total"]) + 1
                        ohtm_file["corpus"][archive_id][interview_id]["sent"] = {}
                        ohtm_file["corpus"][archive_id][interview_id]["model_base"] = {}
                        sent_number = 1
                    for line in interview:
                        text = line[3]
                        text2 = str(text)
                        text_cleaned = re.sub(r"<(.*?)>", " ", text2)
                        ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number] = {}
                        ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["raw"] = str(text_cleaned)
                        ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["speaker"] = {}
                        ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["speaker"] = str(line[2])
                        ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["time"] = {}
                        ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["time"] = str(line[1])
                        if str(line[0]) == "":
                            ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["tape"] = "1"
                        else:
                            ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["tape"] = str(line[0])
                        ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["cleaned"] = {}
                        ohtm_file["corpus"][archive_id][interview_id]["sent"][sent_number]["chunk"] = {}
                        sent_number += 1

    for archive in ohtm_file["corpus"]:
        print(archive)
    ohtm_file = json.dumps(ohtm_file, ensure_ascii=False)
    return ohtm_file
