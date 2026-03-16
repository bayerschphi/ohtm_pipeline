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
load_file_name = "OHD_final_adg_sorted"

ohtm_file = load_json_function(load_file_name, input_folder)

final = []

for sent in ohtm_file["corpus"]["ZWA"]["ZWA465"]["sent"]:
    if ohtm_file["corpus"]["ZWA"]["ZWA465"]["sent"][sent]["chunk"] == 43:
        final.append(ohtm_file["corpus"]["ZWA"]["ZWA465"]["sent"][sent]["cleaned"])
print(final)


