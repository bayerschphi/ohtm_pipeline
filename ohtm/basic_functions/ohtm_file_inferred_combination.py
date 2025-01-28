import copy
from ohtm_pipeline.ohtm.basic_functions.convert_ohtm_file import convert_ohtm_file


def combine_infer(ohtm_file, infer_dic):
    ohtm_file = convert_ohtm_file(ohtm_file)

    infer_dic = convert_ohtm_file(infer_dic)
    for archive in infer_dic["corpus"]:
        if archive not in ohtm_file["corpus"]:
            ohtm_file["corpus"][archive] = {}
            ohtm_file["weight"][archive] = {}
        for interview in infer_dic["corpus"][archive]:
            if interview not in ohtm_file["corpus"][archive]:
                ohtm_file["corpus"][archive][interview] = infer_dic["corpus"][archive][interview]
            if interview not in ohtm_file["weight"][archive]:
                ohtm_file["weight"][archive][interview] = infer_dic["weight"][archive][interview]
    ohtm_file["settings"]["interviews_trained"] = copy.deepcopy(ohtm_file["settings"]["interviews"])
    ohtm_file["settings"]["interviews_inferred"] = copy.deepcopy(infer_dic["settings"]["interviews"])
    ohtm_file["settings"]["inferred"] = copy.deepcopy(infer_dic["settings"]["topic_inferred"])
    ohtm_file["settings"]["topic_modeling"].update({"inferred": "True"})

    # Updating interview numbers for total
    for categories in ohtm_file["settings"]["interviews_inferred"]:
        if categories in ohtm_file["settings"]["interviews"]:
            old_number = copy.deepcopy(int(ohtm_file["settings"]["interviews"][categories]))
            ohtm_file["settings"]["interviews"].update({categories: (
                    old_number + copy.deepcopy(int(ohtm_file["settings"]["interviews_inferred"][categories])))})
        else:
            ohtm_file["settings"]["interviews"][categories] = ohtm_file["settings"]["interviews_inferred"][categories]

    return ohtm_file
