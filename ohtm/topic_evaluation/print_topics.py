import json
import os
from ohtm.basic_functions.convert_ohtm_file import convert_ohtm_file


def print_topic_words_function(ohtm_file, number_of_words: int = 50, topic_words_with_weight:bool = False):
    ohtm_file = convert_ohtm_file(ohtm_file)
    if ohtm_file["settings"]["topic_modeling"]["trained"] == "True":
        for topic_number in ohtm_file["words"]:
            out_line = []
            if topic_words_with_weight:
                for i in range(number_of_words):
                    out_line.append((ohtm_file["words"][topic_number])[i])
            else:
                for i in range(number_of_words):
                    out_line.append((ohtm_file["words"][topic_number])[i][1])
            print("Topic " + str(topic_number) + ": ")
            print(out_line)
    else:
        print("No Topic Model trained")

def save_topic_words(ohtm_file, working_folder: str = "", save_name: str = "", number_of_words: int = 50,
                     topic_words_with_weight:bool = False):
    ohtm_file = convert_ohtm_file(ohtm_file)
    if ohtm_file["settings"]["topic_modeling"]["trained"] == "True":
        out = open(os.path.join(working_folder, save_name + "_topic_words_" + str(number_of_words)
                                + "_words" + '.txt'), 'w', encoding='UTF-8')
        for topic_number in ohtm_file["words"]:
            out_line = []
            if topic_words_with_weight:
                for i in range(number_of_words):
                    out_line.append((ohtm_file["words"][topic_number])[i])
            else:
                for i in range(number_of_words):
                    out_line.append((ohtm_file["words"][topic_number])[i][1])
            out.write(str(topic_number) + " ")
            out.write(str(out_line) + "\n")
            out.write("\n")
        out.close()
    else:
        print("No Topic Model trained")