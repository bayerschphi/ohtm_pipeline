
from ohtm_pipeline.basic_functions.save_load import save_json_function
from ohtm_pipeline.basic_functions.save_load import load_json_function
from ohtm_pipeline.basic_functions.convert_ohtm_file import convert_ohtm_file
import os


def ohtm_label_upgrade(ohtm_file_name: str = "",
                       working_folder: str = "",
                       label_txt: str = "",
                       create_labels: bool = False,                        
                       ):

    ohtm_file = load_json_function(load_file_name=ohtm_file_name, working_folder=working_folder)
    ohtm_file = convert_ohtm_file(ohtm_file=ohtm_file)
    for settings in ohtm_file: 
        print(settings)

    if create_labels: 
        if "topic_labels" in ohtm_file:
            ohtm_file["topic_labels"] = {}
            ohtm_file["topic_labels"]["labels"] = {}
            ohtm_file["topic_labels"]["clusters"] = {}
        else: 
            ohtm_file["topic_labels"] = {}        
        with open(os.path.join(working_folder, label_txt), encoding='UTF-8', mode='r') as file: 
            zeilen = file.readlines()
        for line in zeilen: 
            ohtm_file["topic_labels"]["labels"][line.split(": ")[0]] = line.split(": ")[1].split("\n")[0]

    print(ohtm_file["topic_labels"]["labels"])
    for settings in ohtm_file: 
        print(settings)





    save_json_function(
                        ohtm_file=ohtm_file,
                        working_folder=working_folder,
                        save_name=ohtm_file_name,
                        )
    
