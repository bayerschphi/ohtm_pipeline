"""

The function search for the letter e in the chunk values, because very small weight are
written as: 9.575094194142109e-05. So we filter this numbers out, because they are so low and don't meter.

"""


import copy
from ohtm.basic_functions.convert_ohtm_file import convert_ohtm_file


def print_chunk(ohtm_file, interview_id: str = "", chunk_number: int = 0):
    ohtm_file = convert_ohtm_file(ohtm_file)
    if ohtm_file["settings"]["topic_modeling"]["trained"] == "True":
        chunk_for_print = []
        for archive in ohtm_file["corpus"]:
            if interview_id in ohtm_file["corpus"][archive]:
                for sentence in ohtm_file["corpus"][archive][interview_id]["sent"]:
                    if ohtm_file["corpus"][archive][interview_id]["sent"][sentence]["chunk"] == chunk_number:
                        chunk_for_print.append(ohtm_file["corpus"][archive][interview_id]["sent"][sentence]["raw"])
                print("\n" + "Archive: " + str(archive))
                print("Interview: " + str(interview_id))
                print("Chunk number: " + str(chunk_number))
                print(chunk_for_print)
    else:
        print("No Topic Model trained")


def print_chunk_with_weight_search(ohtm_file, topic_search: int = 0, chunk_weight: float = 0.3):
    ohtm_file = convert_ohtm_file(ohtm_file)
    if ohtm_file["settings"]["topic_modeling"]["trained"] == "True":
        sent_final = []
        for archive in ohtm_file["weight"]:
            for interview in ohtm_file["weight"][archive]:
                for chunks in ohtm_file["weight"][archive][interview]:
                    if str(ohtm_file["weight"][archive][interview][chunks][str(topic_search)]) >= str(chunk_weight):
                        if "e" in str(ohtm_file["weight"][archive][interview][chunks][str(topic_search)]):
                            next
                        else:
                            sent_id = interview
                            chunk_id = chunks
                            sent_current = []
                            for number in ohtm_file["corpus"][archive][interview]["sent"]:
                                int_sent = copy.deepcopy(ohtm_file["corpus"][archive][interview]["sent"][number]["chunk"])
                                if int(int_sent) == int(chunks):
                                    sent_current.append(str(ohtm_file["corpus"][archive][interview]["sent"][number]["raw"]) + " ")
                            sent_current = " ".join(sent_current)
                            sent_current_2 = (str(ohtm_file["weight"][archive][interview][chunks][str(topic_search)]),
                                              sent_id, chunk_id, sent_current)
                            sent_final.append(sent_current_2)
        print("\n" + "The Topic Nr. " + str(topic_search) + " above " + str(chunk_weight) + " was found in this chunks:")
        for interview in sent_final:
            print(interview)
    else:
        print("No Topic Model trained")


def print_chunk_with_interview_weight_search(ohtm_file, interview_id: str = "", topic_search: int = 0,
                                             chunk_weight: float = 0.3):
    ohtm_file = convert_ohtm_file(ohtm_file)
    if ohtm_file["settings"]["topic_modeling"]["trained"] == "True":
        dff = {}
        for archive in ohtm_file["weight"]:
            if interview_id in ohtm_file["weight"][archive]:
                sent_final = []
                for chunks in ohtm_file["weight"][archive][interview_id]:
                    if str(ohtm_file["weight"][archive][interview_id][chunks][str(topic_search)]) >= str(chunk_weight):
                        if "e" in str(ohtm_file["weight"][archive][interview_id][chunks][str(topic_search)]):
                            next
                        else:
                            chunk_id = chunks
                            sent_current = []
                            for sents in ohtm_file["corpus"][archive][interview_id]["sent"]:
                                int_sent = copy.deepcopy(
                                    ohtm_file["corpus"][archive][interview_id]["sent"][sents]["chunk"])
                                if int(int_sent) == int(chunks):
                                    sent_current.append(
                                        str(ohtm_file["corpus"][archive][interview_id]["sent"][sents]["raw"]) + " ")
                            sent_current = " ".join(sent_current)
                            sent_current_2 = (
                                str(ohtm_file["weight"][archive][interview_id][chunks][str(topic_search)]),
                                interview_id, chunk_id, sent_current)
                            sent_final.append(sent_current_2)
                print("\n" + "The topic Nr. " +
                      str(topic_search) + " was found in " + str(interview_id) + " within this chunks:")
                for sent in sent_final:
                    print(sent)
    else:
        print("No Topic Model trained")

