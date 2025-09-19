"""
OHTM-Pipeline:

With this board you can select every option for your topic model.
You can set the different options on and off via "True" and "False".

First set the required paths.
    - the first "mallet_path" to your mallet directory.
     (see https://programminghistorian.org/en/lessons/topic-modeling-and-mallet)
    - the second one to your output_folder. This folder is your working environment.
      All models are saved there and can be loaded from this folder.
    - your stopword file must be stored in this output_folder.
"""

import os
from ohtm_pipeline.pipeline_function.upgrade_and_labeling import ohtm_label_upgrade

''' Path Settings: '''

# Path to your output_folder.
working_folder: str = (r"C:\Users\bayerschmidt\sciebo - Bayerschmidt,"
                       r" Philipp (bayerschmidt@fernuni-hagen.de)@fernuni-hagen.sciebo.de\Topic Modeling\ohtm_files")


""" Upgrade Settings: """

ohtm_file_name = "ohtm_100c_120T_final"



""" Create Topic Labels """
create_labels = True
topic_label_file_name = "topic_labels_template.txt"


if __name__ == "__main__":
    ohtm_label_upgrade(
        ohtm_file_name = ohtm_file_name,
        working_folder = working_folder,
        label_txt = topic_label_file_name,
        create_labels = create_labels, 

    )