
from ohtm_pipeline.basic_functions.save_load import save_json_function
from ohtm_pipeline.basic_functions.save_load import load_json_function
from ohtm_pipeline.basic_functions.convert_ohtm_file import convert_ohtm_file
import os


def ohtm_label_upgrade(ohtm_file_name: str = "",
                       working_folder: str = "",
                       label_txt: str = "",
                       create_labels: bool = False,
                       create_clusters: bool = False, 
                       cluster_txt: str = "",                     
                       ):

    ohtm_file = load_json_function(load_file_name=ohtm_file_name, working_folder=working_folder)
    ohtm_file = convert_ohtm_file(ohtm_file=ohtm_file)

    if "labeling_options" not in ohtm_file["settings"]:
        ohtm_file["settings"]["labeling_options"] = {}
        ohtm_file["settings"]["labeling_options"]["labeling"] = False
        ohtm_file["settings"]["labeling_options"]["clustering"] = False

    
    if create_labels: 
        if "topic_labels" not in ohtm_file:
            ohtm_file["topic_labels"] = {}
            ohtm_file["topic_labels"]["labels"] = {}

        else: 
            ohtm_file["topic_labels"]["labels"] = {}        
        with open(os.path.join(working_folder, label_txt), encoding='UTF-8', mode='r') as file: 
            zeilen = file.readlines()
        for line in zeilen: 
            ohtm_file["topic_labels"]["labels"][line.split(": ")[0]] = line.split(": ")[0] + " - " + line.split(": ")[1].split("\n")[0]
        ohtm_file["settings"]["labeling_options"]["labeling"] = True


    if create_clusters: 
        if "topic_labels" not in ohtm_file:
            ohtm_file["topic_labels"] = {}
        if "clusters" in ohtm_file["topic_labels"]:
            ohtm_file["topic_labels"]["clusters"] = {}
        else:
            ohtm_file["topic_labels"]["clusters"] = {}
        with open(os.path.join(working_folder, cluster_txt), encoding='UTF-8', mode='r') as file: 
            zeilen = file.readlines()
        
        for lines in zeilen: 
            ohtm_file["topic_labels"]["clusters"][lines.split(": ")[0]] = (lines.split(": ")[1].split(" - ")[0], lines.split(": ")[1].split(" - ")[1].split("\n")[0])
        ohtm_file["settings"]["labeling_options"]["clustering"] = True

    save_json_function(
                        ohtm_file=ohtm_file,
                        working_folder=working_folder,
                        save_name=ohtm_file_name,
                        )
    
