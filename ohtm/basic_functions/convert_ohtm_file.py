"""
For later use, we have to save the ohtm_file as a json file. But inside the code, the ohtm_file has to
be a python dictionary. This function helps, to check, if the ohtm_file has the right form.

"""

import json


# The code has to check, if the json file was loaded as a json file. If so, it has to be returned to a dictionary.
def convert_ohtm_file(ohtm_file):
    if type(ohtm_file) is not dict:
        ohtm_file = json.loads(ohtm_file)
    else:
        ohtm_file = ohtm_file
    return ohtm_file
