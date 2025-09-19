"""
With this function you can set custome labels to eacht topic and further more create 
clusters with individual names for topic combinations.

For that you have to create a .TXT file each for the labels and the clusters in the format
given inside this repository. Than put those files in the same folder, as your ohtm_files is
and set the wantes options and run the script.
"""

import os
from ohtm_pipeline.pipeline_function.upgrade_and_labeling import ohtm_label_upgrade

''' Path Settings: '''

# Path to your output_folder.
working_folder: str = (r"C:\Users\bayerschmidt\sciebo - Bayerschmidt,"
                       r" Philipp (bayerschmidt@fernuni-hagen.de)@fernuni-hagen.sciebo.de\Topic Modeling\ohtm_files")


""" Upgrade Settings: """

ohtm_file_name = "OHD_final_adg_sorted_test"


""" Create Topic Labels """
create_labels = True
topic_label_file_name = "topic_labels_template.txt"


""" Create Topic Clusters """
create_clusters = True
topic_cluster_file_name = "clustering.txt"


if __name__ == "__main__":
    ohtm_label_upgrade(
        ohtm_file_name = ohtm_file_name,
        working_folder = working_folder,
        label_txt = topic_label_file_name,
        create_labels = create_labels,
        cluster_txt = topic_cluster_file_name,
        create_clusters=create_clusters 

    )