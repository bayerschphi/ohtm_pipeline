"""
In order to calculate your topic model, the whole documents have to be shortn.
For this we split the text into shorter documents, called chunks.
The chunks are build by adding words until the maximum (chunk_setting) is reached.
"""

import json
import copy
from ohtm_pipeline.basic_functions.convert_ohtm_file import convert_ohtm_file



def chunking(ohtm_file, chunk_setting: int = 0):
    ohtm_file = convert_ohtm_file(ohtm_file)
    print(chunk_setting)
    if chunk_setting != 0:
        for archive in ohtm_file["corpus"]:
            for interview in ohtm_file["corpus"][archive]:
                chunk_count = 0
                chunk_data = []
                for nr in range(1, (len(ohtm_file["corpus"][archive][interview]["sent"]) + 1)):
                    new_sent = copy.deepcopy(ohtm_file["corpus"][archive][interview]["sent"][str(nr)]["cleaned"])
                    if len(chunk_data) + len(new_sent) >= chunk_setting:
                        if len(chunk_data) + len(new_sent) >= chunk_setting + (chunk_setting/5):
                            chunk_count += 1
                            ohtm_file["corpus"][archive][interview]["sent"][str(nr)]["chunk"] = chunk_count
                            chunk_data = new_sent
                        else:
                            ohtm_file["corpus"][archive][interview]["sent"][str(nr)]["chunk"] = chunk_count
                            chunk_data += ohtm_file["corpus"][archive][interview]["sent"][str(nr)]["cleaned"]
                            chunk_count += 1
                            chunk_data = []
                    else:
                        ohtm_file["corpus"][archive][interview]["sent"][str(nr)]["chunk"] = chunk_count
                        chunk_data += new_sent

        ohtm_file["settings"]["preprocessing"].update({"chunk_setting": chunk_setting})
        ohtm_file["settings"]["preprocessing"].update({"chunked": "True"})

        ohtm_file = json.dumps(ohtm_file, ensure_ascii=False)
    else:
        for archive in ohtm_file["corpus"]:
            for interview in ohtm_file["corpus"][archive]:
                for nr in ohtm_file["corpus"][archive][interview]["sent"]:
                    ohtm_file["corpus"][archive][interview]["sent"][str(nr)]["chunk"] = 0

        ohtm_file["settings"]["preprocessing"].update({"chunk_setting": chunk_setting})
        ohtm_file["settings"]["preprocessing"].update({"chunked": "False"})

        ohtm_file = json.dumps(ohtm_file, ensure_ascii=False)

    return ohtm_file
