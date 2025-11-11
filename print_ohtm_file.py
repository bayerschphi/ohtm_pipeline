"""
With this function you can access the different levels inside the ohtm_file.
It is a nested dictionary, every bracket is a different key for a different level.
"""

import ohtm_pipeline
from ohtm_pipeline.basic_functions.save_load import load_json_function
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

input_folder: str = (r"C:\Users\phili\sciebo - Bayerschmidt,"
                       r" Philipp (bayerschmidt@fernuni-hagen.de)@fernuni-hagen.sciebo.de\Topic Modeling\ohtm_files")
load_file_name = "OHD_final_100c_100T_A5_final"

ohtm_file = load_json_function(load_file_name, input_folder)

for sents in ohtm_file["corpus"]["ADG"]["ADG1806"]["sent"]:
    if ohtm_file["corpus"]["ADG"]["ADG1806"]["sent"][sents]["chunk"] == 7:
        print(ohtm_file["corpus"]["ADG"]["ADG1806"]["sent"][sents]["cleaned"])

