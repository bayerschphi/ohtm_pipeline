import copy
import json

def combine_infer(top_dic, infer_dic):
    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic

    if type(infer_dic) is not dict:
        infer_dic = json.loads(infer_dic)
    else:
        infer_dic = infer_dic


    for archive in infer_dic["corpus"]:
        if archive not in top_dic["corpus"]:
            top_dic["corpus"][archive] = {}
            top_dic["weight"][archive] = {}
        for interview in infer_dic["corpus"][archive]:
            if interview not in top_dic["corpus"][archive]:
                top_dic["corpus"][archive][interview] = infer_dic["corpus"][archive][interview]
            if interview not in top_dic["weight"][archive]:
                top_dic["weight"][archive][interview] = infer_dic["weight"][archive][interview]
    top_dic["settings"]["interviews_trained"] = copy.deepcopy(top_dic["settings"]["interviews"])
    top_dic["settings"]["interviews_inferred"] = copy.deepcopy(infer_dic["settings"]["interviews"])
    top_dic["settings"]["inferred"] = copy.deepcopy(infer_dic["settings"]["topic_inferred"])
    top_dic["settings"]["topic_modeling"].update({"inferred": "True"})

    # Updating interview numbers for total
    for categories in top_dic["settings"]["interviews_inferred"]:
        if categories in top_dic["settings"]["interviews"]:
            old_number = copy.deepcopy(int(top_dic["settings"]["interviews"][categories]))
            top_dic["settings"]["interviews"].update({categories: (old_number + copy.deepcopy(int(top_dic["settings"]["interviews_inferred"][categories])))})
        else:
            top_dic["settings"]["interviews"][categories] = top_dic["settings"]["interviews_inferred"][categories]

    return top_dic
