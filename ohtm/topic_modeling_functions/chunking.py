import json
import copy


def chunking(top_dic, chunk_setting: int=0):

    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic

    for archive in top_dic["corpus"]:
        for interview in top_dic["corpus"][archive]:
            chunk_count = 0
            chunk_data = []
            for nr in range(1, (len(top_dic["corpus"][archive][interview]["sent"]) + 1)):
                new_sent = copy.deepcopy(top_dic["corpus"][archive][interview]["sent"][str(nr)]["cleaned"])
                if len(chunk_data) + len(new_sent) >= chunk_setting:
                    if len(chunk_data) + len(new_sent) >= chunk_setting + (chunk_setting/5):
                        chunk_count += 1
                        top_dic["corpus"][archive][interview]["sent"][str(nr)]["chunk"] = chunk_count
                        chunk_data = new_sent
                    else:
                        top_dic["corpus"][archive][interview]["sent"][str(nr)]["chunk"] = chunk_count
                        chunk_data += top_dic["corpus"][archive][interview]["sent"][str(nr)]["cleaned"]
                        chunk_count += 1
                        chunk_data = []
                else:
                    top_dic["corpus"][archive][interview]["sent"][str(nr)]["chunk"] = chunk_count
                    chunk_data += new_sent

    top_dic["settings"]["preprocessing"].update({"chunk_setting": chunk_setting})
    top_dic["settings"]["preprocessing"].update({"chunked": "True"})

    top_dic = json.dumps(top_dic, ensure_ascii=False)

    return top_dic