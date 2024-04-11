'''
This function converts primary interviews from  .txt .ods and .csv files into the data structure for this topic modeling pipeline, called top_dic.
The csv. and .ods files are optimized for the structure of the online archive oral-history.digital.
The txt files are special structured. [ergänzen]

If you only have a plane text, just set speaker_txt to False. Then each sentence is split by punctuation and will be loaded.

The archive name and the interview id are build from the file name. The first 3 letters are used for the archive, and the hole
name is used for the id.

Datastructure:

top_dc:
    corpus:
        archive1
        archive2
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




'''


import os
import re
import json
import csv
import pandas as pd


def dictionary_creation(source: str = "", speaker_txt: bool = True):

    top_dic = {}

    top_dic["corpus"] = {}
    top_dic["weight"] = {}
    top_dic["words"] = {}
    top_dic["stopwords"] = {}
    top_dic["correlation"] = {}
    top_dic["settings"] = {}
    top_dic["settings"]["interviews"] = {}
    top_dic["settings"]["interviews"]["total"] = 0
    top_dic["settings"]["preprocessing"] = {}
    top_dic["settings"]["preprocessing"]["preprocessed"] = "False"
    top_dic["settings"]["preprocessing"]["stopwords_removed"] = "False"
    top_dic["settings"]["preprocessing"]["lemma"] = "False"
    top_dic["settings"]["preprocessing"]["chunked"] = "False"
    top_dic["settings"]["preprocessing"]["chunk_setting"] = "None"
    top_dic["settings"]["topic_modeling"] = {}
    top_dic["settings"]["topic_modeling"]["trained"] = "False"


    for folder in source:
        for file in os.listdir(folder):
            print(file)
            print(file.split(".")[1])

            # Ich bin mir unsicher, ob es diese verschiedenen Codierungen brauch
            if file.split(".")[1] == "txt":
                try:
                    text = open(folder + '\\' + file, 'r', encoding='UTF-8-sig').read()
                except UnicodeDecodeError:
                    try:
                        text = open(folder + '\\' + file, 'r', encoding='UTF-8').read()
                    except UnicodeDecodeError:
                        try:
                            text = open(folder + '\\' + file, 'r', encoding='UTF-16-le').read()
                        except UnicodeDecodeError:
                            try:
                                text = open(folder + '\\' + file, 'r', encoding='UTF-16-be').read()
                            except UnicodeDecodeError:
                                text = open(folder + '\\' + file, 'r', encoding='ANSI').read()
                                text = text.encode('UTF-8')
                                text = text.decode('UTF-8', 'ignore')

                text_unified = text.replace('!', '. ').replace('?', '. ').replace(';', '. ').replace('...,', ', ').replace(
                    '..,', ', ').replace('"', ' ').replace("'", ' ').replace(" - ", " ")
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

                sent_number = 1
                for line in text_split:
                    if len(line) == 0:
                        next
                    else:
                        if speaker_txt == True:
                            try:
                                speaker = re.findall(r"^\*(.*?)\*[ ]", line)[0]
                            except IndexError:
                                speaker = speaker

                        text = re.sub(r"\*(.*?)\*[ ]", "", line)
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


            if file.split(".")[1] == "ods":
                interview = pd.read_excel(folder + "\\" + file)
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
                    sent_number = 1
                for line in interview:
                    text = line[2]
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number] = {}
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["raw"] = str(text)
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["speaker"] = {}
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["speaker"] = str(line[1])
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["time"] = {}
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["time"] = str(line[0])
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["tape"] = {}
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["tape"] = file.split(".")[0].split("_")[2][1]
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["cleaned"] = {}
                    top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["chunk"] = {}
                    sent_number += 1

            if file.split(".")[1] == "csv":
                with open(folder + "\\" + file, 'r', newline='', encoding='utf-8') as csvfile:
                    interview = csv.reader(csvfile, delimiter="\t", quotechar= None)
                    next(interview) #Um die erste Zeile in der .csv zu überspringen
                    interview_id = file.split(".")[0].split("_")[0]
                    if file[:3] not in top_dic["corpus"]:
                        top_dic["corpus"][file[:3]] = {}
                        top_dic["settings"]["interviews"][file[:3]] = 0
                    if interview_id not in top_dic["corpus"][file[:3]]:
                        top_dic["corpus"][file[:3]][interview_id] = {}
                        top_dic["settings"]["interviews"][file[:3]] = (top_dic["settings"]["interviews"][file[:3]]) + 1
                        top_dic["settings"]["interviews"]["total"] = (top_dic["settings"]["interviews"]["total"]) + 1
                        top_dic["corpus"][file[:3]][interview_id]["sent"] = {}
                        sent_number = 1
                    for line in interview:
                        text = line[3]
                        text = re.sub(r"\<(.*?)\>[ ]", "", text)
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number] = {}
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["raw"] = str(text)
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["speaker"] = {}
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["speaker"] = str(line[2])
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["time"] = {}
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["time"] = str(line[1])
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["tape"] = str(line[0])
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["cleaned"] = {}
                        top_dic["corpus"][file[:3]][interview_id]["sent"][sent_number]["chunk"] = {}
                        sent_number += 1

    top_dic = json.dumps(top_dic, ensure_ascii=False)
    return top_dic
