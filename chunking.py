
def chunking(top_dic, chunk_setting):
    import json
    import copy

    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic

    for archiv in top_dic["korpus"]:
        for ID in top_dic["korpus"][archiv]:
            chunk_count = 1
            chunk_data = []
            for nr in range(1, (len(top_dic["korpus"][archiv][ID]["sent"]) + 1)):
                new_sent = copy.deepcopy(top_dic["korpus"][archiv][ID]["sent"][str(nr)]["cleaned"])
                if len(chunk_data) + len(new_sent) >= chunk_setting:
                    if len(chunk_data) + len(new_sent) >= chunk_setting + (chunk_setting/5):
                        chunk_count += 1
                        top_dic["korpus"][archiv][ID]["sent"][str(nr)]["chunk"] = chunk_count
                        chunk_data = new_sent
                    else:
                        top_dic["korpus"][archiv][ID]["sent"][str(nr)]["chunk"] = chunk_count
                        chunk_data += top_dic["korpus"][archiv][ID]["sent"][str(nr)]["cleaned"]
                        chunk_count += 1
                        chunk_data = []
                else:
                    top_dic["korpus"][archiv][ID]["sent"][str(nr)]["chunk"] = chunk_count
                    chunk_data += new_sent


    top_dic["settings"].update({"chunk_setting": chunk_setting})

    top_dic = json.dumps(top_dic)

    return top_dic