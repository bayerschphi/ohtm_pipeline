import json
import pickle
import copy
from datetime import datetime
import re
import gensim
import pandas as pd
import json


def print_topic_words(topic_dictionary, number_of_words, name_dataset, save_doc=False):
    now = str(datetime.now())[:19]
    now_formatted = now[2:4] + now[5:7] + now[8:10] + now[11:13] + now[14:16] + now[17:19]
    now = now_formatted

    if type(topic_dictionary) is not dict:
        top_dic = json.loads(topic_dictionary)
    else:
        top_dic = topic_dictionary

    word_dic = {}

    if save_doc:
                out = open('keywords_mallet_' + name_dataset + '_'+ 'topics_' + str(number_of_words) + 'keywords' + now + '.txt', 'w',
                           encoding='UTF-8')
                for top_words in top_dic["words"]:
                    out_line = []
                    for i in range(number_of_words):
                        out_line.append((top_dic["words"][top_words])[i][1])
                    out.write("Topic " + "\n" + str(top_words) + "\n")
                    out.write(str(out_line) + "\n")
                    out.write("\n")
                    word_dic[top_words] = out_line
                out.close

    else:
                for top_words in top_dic["words"]:
                    out_line = []
                    for i in range(number_of_words):
                        out_line.append((top_dic["words"][top_words])[i][1])
                    word_dic[top_words] = out_line

    pd.set_option('display.max_colwidth', None)

    words_df = pd.DataFrame([', '.join([term for term in word_dic[topic]]) for topic in word_dic], columns = ['Terms per Topic'], index=['Topic'+str(topic) for topic in word_dic])
    words_df.style.set_properties(**{'text-align': 'left'})


def save_topic_words(top_dic, working_folder: str = "", save_name: str = "", number_of_words: int = 50):
    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic

    out = open(working_folder + save_name + "top_words_" "50_words_2" + '.txt', 'w', encoding='UTF-8')
    number_of_words
    for top_words in top_dic["words"]:
        out_line = []
        for i in range(number_of_words):
            out_line.append((top_dic["words"][top_words])[i][1])
        out.write(str(top_words) + " ")
        out.write(str(out_line) + "\n")
        out.write("\n")

    out.close

def print_chunk(top_dic, interview_id:str="", chunk_number:int=0):
    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic
    chunk_for_print =[]
    for sentence in top_dic["corpus"][interview_id[:3]][interview_id]["sent"]:
        if top_dic["corpus"][interview_id[:3]][interview_id]["sent"][sentence]["chunk"] == chunk_number:
            chunk_for_print.append(top_dic["corpus"][interview_id[:3]][interview_id]["sent"][sentence]["raw"])

    print(chunk_for_print)


def print_chunk_with_weight_search(top_dic, topic_search: int = 0, chunk_weight: float = 0.3):
    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic

    sent_final = []
    for a in top_dic["weight"]:
        for i in top_dic["weight"][a]:
            for chunks in top_dic["weight"][a][i]:
                if str(top_dic["weight"][a][i][chunks][str(topic_search)]) >= str(chunk_weight):
                    sent_id = i
                    chunk_id = chunks
                    sent_current = []
                    for sents in top_dic["corpus"][a][i]["sent"]:
                        int_sent = copy.deepcopy(top_dic["corpus"][a][i]["sent"][sents]["chunk"])
                        if int(int_sent) == int(chunks):
                            sent_current.append(str(top_dic["corpus"][a][i]["sent"][sents]["raw"]) + " ")
                    sent_current = " ".join(sent_current)
                    sent_current_2 = (str(top_dic["weight"][a][i][chunks][str(topic_search)]), sent_id, chunk_id, sent_current)
                    sent_final.append(sent_current_2)
    for i in sent_final:
        print(i)



def print_chunk_with_interview_weight_search(top_dic, interview_id:str="", topic_search: int = 0, chunk_weight: float = 0.3):
    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic

    sent_final = []
    a = interview_id[:3]
    i = interview_id
    for chunks in top_dic["weight"][a][i]:
        if str(top_dic["weight"][a][i][chunks][str(topic_search)]) >= str(chunk_weight):
            chunk_id = chunks
            sent_current = []
            for sents in top_dic["corpus"][a][i]["sent"]:
                int_sent = copy.deepcopy(top_dic["corpus"][a][i]["sent"][sents]["chunk"])
                if int(int_sent) == int(chunks):
                    sent_current.append(str(top_dic["corpus"][a][i]["sent"][sents]["raw"]) + " ")
            sent_current = " ".join(sent_current)
            sent_current_2 = (str(top_dic["weight"][a][i][chunks][str(topic_search)]), i, chunk_id, sent_current)
            sent_final.append(sent_current_2)
    for i in sent_final:
        print(i)

