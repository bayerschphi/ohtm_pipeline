# In dieser Version wird unterschieden, ob es sich bei den Transkripten um .txt oder .ods Dateien handelt.
# das ist wichtig, weil die .ods Dateien die von OHD kommen Metadaten enthalten, die für die analyse später berücksichtig werden sollen.


def json_creation(stoplist_path, working_folder, source, Save = False):
    import os
    import re
    import json
    import pandas as pd
    import copy
    import csv
    from main_pipeline.bayerschmidt_topic_modeling import preprocess_outstr


    top_dic = {}

    top_dic["korpus"] = {}
    top_dic["weight"] = {}
    top_dic["words"] = {}
    top_dic["settings"] = {}
    top_dic["settings"]["interviews"] = {}

    for folder in source:
        for file in os.listdir(folder):
            print(file)
            print(file.split(".")[1])
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

                # Dieser Teil ist für später irrelevant. Ist nur für meine eigene Textstruktur wichtig.
                text = re.sub(r"\*(.*?)\*[ ]", "", text)
                text = re.sub(r"\((.*?)\)[ ]", "", text)
                text = re.sub(r"\((.*?)\)", "", text)
                text = re.sub(r"(.*\n.*\n.*\n.*\n.*\n)(\+\+)", "", text)
                text = re.sub(r"^[ ]", "", text)

                text_unified = text.replace('!', '.').replace('?', '.').replace(';', '.').replace('...,', ',').replace(
                    '..,', ',').replace('"', '').replace("'", '').replace("\n", ' ').replace(" - ", " ")
                text_split = text_unified.split('. ')

                id = file.split(".")[0]
                if file[:3] not in top_dic["korpus"]:
                    top_dic["korpus"][file[:3]] = {}
                    top_dic["settings"]["interviews"][file[:3]] = 0
                top_dic["korpus"][file[:3]][id] = {}
                top_dic["settings"]["interviews"][file[:3]] = (top_dic["settings"]["interviews"][file[:3]])+1
                top_dic["korpus"][file[:3]][id]["sent"] = {}

                sent_number = 1
                for sent in text_split:
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number] = {}
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number]["raw"] = sent
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number]["time"] = {}
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number]["band"] = {}
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number]["cleaned"] = {}
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number]["speaker"] = {}
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number]["chunk"] = {}

                    sent_number += 1
            if file.split(".")[1] == "ods":
                df = pd.read_excel(folder + "\\" + file)
                df = df.values.tolist()
                id = file.split(".")[0].split("_")[0]
                if file[:3] not in top_dic["korpus"]:
                    top_dic["korpus"][file[:3]] = {}
                    top_dic["settings"]["interviews"][file[:3]] = 0
                if id not in top_dic["korpus"][file[:3]]:
                    top_dic["korpus"][file[:3]][id] = {}
                    top_dic["settings"]["interviews"][file[:3]] = (top_dic["settings"]["interviews"][file[:3]]) + 1
                    top_dic["korpus"][file[:3]][id]["sent"] = {}
                    sent_number = 1
                for i in df:
                    text = i[2]
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number] = {}
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number]["raw"] = text
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number]["speaker"] = {}
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number]["speaker"] = i[1]
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number]["time"] = {}
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number]["time"] = str(i[0]) # scheinbar wurden einige Werte aus den Excel-Tabellen nicht als str übergeben. Das führt zu Probleme, bei der Umwandlung in ein Json. Deswegen werden die Werte als str übergeben
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number]["band"] = {}
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number]["band"] = file.split(".")[0].split("_")[2][1]
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number]["cleaned"] = {}
                    top_dic["korpus"][file[:3]][id]["sent"][sent_number]["chunk"] = {}
                    sent_number += 1

            if file.split(".")[1] == "csv":
                with open(folder + "\\" + file, 'r', newline='', encoding='utf-8') as csvfile:
                    df = csv.reader(csvfile, delimiter="\t")
                    next(df)
                    id = file.split(".")[0].split("_")[0]
                    if file[:3] not in top_dic["korpus"]:
                        top_dic["korpus"][file[:3]] = {}
                        top_dic["settings"]["interviews"][file[:3]] = 0
                    if id not in top_dic["korpus"][file[:3]]:
                        top_dic["korpus"][file[:3]][id] = {}
                        top_dic["settings"]["interviews"][file[:3]] = (top_dic["settings"]["interviews"][file[:3]]) + 1
                        top_dic["korpus"][file[:3]][id]["sent"] = {}
                        sent_number = 1
                    for i in df:
                        text = i[3]
                        top_dic["korpus"][file[:3]][id]["sent"][sent_number] = {}
                        top_dic["korpus"][file[:3]][id]["sent"][sent_number]["raw"] = text
                        top_dic["korpus"][file[:3]][id]["sent"][sent_number]["speaker"] = {}
                        top_dic["korpus"][file[:3]][id]["sent"][sent_number]["speaker"] = i[2]
                        top_dic["korpus"][file[:3]][id]["sent"][sent_number]["time"] = {}
                        top_dic["korpus"][file[:3]][id]["sent"][sent_number]["time"] = str(i[1]) # scheinbar wurden einige Werte aus den Excel-Tabellen nicht als str übergeben. Das führt zu Probleme, bei der Umwandlung in ein Json. Deswegen werden die Werte als str übergeben
                        top_dic["korpus"][file[:3]][id]["sent"][sent_number]["band"] = {}
                        top_dic["korpus"][file[:3]][id]["sent"][sent_number]["band"] = str(i[0])
                        top_dic["korpus"][file[:3]][id]["sent"][sent_number]["cleaned"] = {}
                        top_dic["korpus"][file[:3]][id]["sent"][sent_number]["chunk"] = {}
                        sent_number += 1



    stoplist = open(stoplist_path, encoding='UTF-16', mode='r').read().split()

    # Stopwords werden entfernt und unter "cleaned" als Token eingefügt.

    def remove_stopwords_by_list(data, stoplist):
        data_out = [[word for word in line if word not in stoplist] for line in data]
        return data_out

    sent_length = []
    for archiv in top_dic["korpus"]:
        for ID in top_dic["korpus"][archiv]:
            for nr in top_dic["korpus"][archiv][ID]["sent"]:
                text = copy.deepcopy(top_dic["korpus"][archiv][ID]["sent"][nr]["raw"])
                try:
                    text_unified = text.replace('!', '.').replace('?', '.').replace(';', '.').replace('...,',
                                                                                                      ',').replace(
                        '..,', ',').replace('"', '').replace("'", '').replace("\n", ' ').replace(" - ", " ")
                except:
                    text_unified = i[2]
                text = text_unified
                pre_line = preprocess_outstr(text)
                line = pre_line.split(" ")
                data_out = [word for word in line if word not in stoplist]
                data_out2 = [word for word in data_out if len(word) > 2]
                top_dic["korpus"][archiv][ID]["sent"][nr]["cleaned"] = data_out2
                sent_length.append(len(data_out2))

    sent_length = [word for word in sent_length if word is not 0]
    sent_length.sort()
    max_length = sent_length[-1]
    min_length = sent_length[0]
    average_length = sum(sent_length)/len(sent_length)


    top_dic["settings"]["cleaned_length"] = {}
    top_dic["settings"]["cleaned_length"]["max_length"] = max_length
    top_dic["settings"]["cleaned_length"]["ave_length"] = average_length

    top_dic = json.dumps(top_dic)
    if Save == True:
        with open(working_folder + "adg3.json", "w", encoding="utf-8") as f:
            json.dump(top_dic, f)



    return top_dic
