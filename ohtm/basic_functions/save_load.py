import json
import os

def save_json_function(top_dic, working_folder:str = "", save_name:str = ""):
    folder_path = os.path.join(working_folder)
    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic
    with open(os.path.join(folder_path, save_name + ".json"), "w", encoding="utf-8") as f:
        json.dump(top_dic, f)
        print(f"The json was saved in the Folder '{save_name}' as '{save_name}.json'")


def load_json_function(load_file_name:str="", working_folder:str=""):
    with open(os.path.join(working_folder, load_file_name + ".json")) as f:
        top_dic = json.load(f)
        if type(top_dic) is not dict:
            top_dic = json.loads(top_dic)
        else:
            top_dic = top_dic
        print(f"The json '{load_file_name}.json' was loaded")
        return top_dic
