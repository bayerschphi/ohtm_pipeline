"""
With this function you can access the different levels inside the ohtm_file.
It is a nested dictionary, every bracket is a different key for a different level.
"""

import ohtm_pipeline
from ohtm_pipeline.ohtm.basic_functions.save_load import load_json_function
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

input_folder: str = (r"C:\Users\phili\sciebo - Bayerschmidt,"
                       r" Philipp (bayerschmidt@fernuni-hagen.de)@fernuni-hagen.sciebo.de\Topic Modeling\ohtm_files")
load_file_name = "ohtm_100c_120T"

ohtm_file = load_json_function(load_file_name, input_folder)

print(ohtm_file["stopwords"])
