import json
import os
from ohtm_pipeline.basic_functions.convert_ohtm_file import convert_ohtm_file


def save_json_function(ohtm_file, working_folder: str = "", save_name: str = ""):
    folder_path = os.path.join(working_folder)
    ohtm_file = convert_ohtm_file(ohtm_file)
    with open(os.path.join(folder_path, save_name + ".ohtm"), "w", encoding="utf-8") as f:
        json.dump(ohtm_file, f)
        print(f"The ohtm_file was saved in the Folder '{save_name}.ohtm'")


def load_json_function(load_file_name: str = "", working_folder: str = ""):
    with open(os.path.join(working_folder, load_file_name + ".ohtm")) as f:
        ohtm_file = json.load(f)
        ohtm_file = convert_ohtm_file(ohtm_file)
        print(f"The ohtm_file '{load_file_name}.ohtm' was loaded")
        return ohtm_file


def save_topic_words(ohtm_file, working_folder: str = "", save_name: str = "", number_of_words: int = 50):
    ohtm_file = convert_ohtm_file(ohtm_file)
    if ohtm_file["settings"]["topic_modeling"]["trained"] == "True":
        out = open(os.path.join(working_folder, save_name + "_topic_words_" + str(number_of_words)
                                + "_words" + '.txt'), 'w', encoding='UTF-8')
        for top_words in ohtm_file["words"]:
            out_line = []
            for i in range(number_of_words):
                out_line.append((ohtm_file["words"][top_words])[i][1].lower())
            out.write(str(top_words) + " ")
            out.write(str(out_line) + "\n")
            out.write("\n")
        out.close()
    else:
        print("No Topic Model trained")