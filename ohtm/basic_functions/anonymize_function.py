'''Function to anonymze the ohtm_file from all relevant text in raw, cleaned and speaker'''

from ohtm.basic_functions.convert_ohtm_file import convert_ohtm_file
import json

def anonymize_function(ohtm_file, exceptions):
    ohtm_file = convert_ohtm_file(ohtm_file)
    for archive in ohtm_file["corpus"]:
        for interview in ohtm_file["corpus"][archive]:
            if interview in exceptions:
                ohtm_file["corpus"][archive][interview]["anonymized"] = "False"
            else:
                ohtm_file["corpus"][archive][interview]["anonymized"] = "True"
                for sent in ohtm_file["corpus"][archive][interview]["sent"]:
                    ohtm_file["corpus"][archive][interview]["sent"][sent]["raw"] = "anonymized"
                    ohtm_file["corpus"][archive][interview]["sent"][sent]["cleaned"] = ["anonymized"]
                    ohtm_file["corpus"][archive][interview]["sent"][sent]["speaker"] = "anonymized"
    ohtm_file["settings"]["anonymized"] = {}
    ohtm_file["settings"]["anonymized"]["anonymized"] = "True"
    ohtm_file["settings"]["anonymized"]["exceptions"] = exceptions
    ohtm_file = json.dumps(ohtm_file, ensure_ascii=False)

    return ohtm_file