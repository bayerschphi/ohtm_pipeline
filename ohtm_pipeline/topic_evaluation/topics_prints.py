"""

The function search for the letter e in the chunk values, because very small weight are
written as: 9.575094194142109e-05. So we filter this numbers out, because they are so low and don't meter.


Links are only available for interviews from oral-history.digital
"""


import copy
from ohtm_pipeline.basic_functions.convert_ohtm_file import convert_ohtm_file
from ohtm_pipeline.basic_functions.create_link_to_ohd import create_link

def print_chunk(ohtm_file, interview_id: str = "", chunk_number: int = 0, show_links: bool = False):
    ohtm_file = convert_ohtm_file(ohtm_file)
    anonymized_status = False
    if ohtm_file["settings"]["topic_modeling"]["trained"] == "True":
        sent_example = []
        speaker = "None"
        chunk_start_marker = 0
        link_tape = "1"
        for archive in ohtm_file["corpus"]:
            if interview_id in ohtm_file["corpus"][archive]:
                try:
                    if ohtm_file["corpus"][archive][interview_id]["anonymized"] == "True":
                        anonymized_status = True
                except KeyError:
                    anonymized_status = False
                for sentence_number in ohtm_file["corpus"][archive][interview_id]["sent"]:
                    if ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["chunk"] == chunk_number:
                        chunk_start_marker +=1
                        if chunk_start_marker == 1: # to mark the beginning of the chunk for the first timecode
                            if ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["time"] != {}:
                                timcodes_available = True
                                chunk_start_time = ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["time"]
                                link_tape = ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["tape"]
                            else:
                                timcodes_available = False
                        if ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["speaker"] == {}:
                            sent_example.append(ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["raw"] + " ")
                            if ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["time"] != {}:
                                chunk_end_time = ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["time"]
                        else:
                            if speaker == ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["speaker"]:
                                sent_example.append(ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["raw"] )
                                if ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["time"] != {}:
                                    chunk_end_time = \
                                    ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["time"]
                            else:
                                sent_example.append("*" + ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["speaker"] + "*: ")
                                sent_example.append(ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["raw"])
                                speaker = ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["speaker"]
                                if ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["time"] != {}:
                                    chunk_end_time = \
                                    ohtm_file["corpus"][archive][interview_id]["sent"][sentence_number]["time"]
                print("\n" + "Archive: " + str(archive))
                print("Interview: " + str(interview_id))
                print("Chunk number: " + str(chunk_number))
                if timcodes_available:
                    print("Timecode: " + str(chunk_start_time) + "–" +str(chunk_end_time))
                else:
                    chunk_start_time = "False"
                    link_tape = "1"
                if anonymized_status:
                    link = create_link(archive.lower(), interview_id.lower(), chunk_start_time, link_tape)
                    print("This interview is anonymized and can be found: " + link)
                else:
                    for sent in sent_example:
                        print(sent)
                    if show_links:
                        link = create_link(archive.lower(), interview_id.lower(), chunk_start_time, link_tape)
                        print(link)
    else:
        print("No Topic Model trained")

def print_chunk_with_weight_search(ohtm_file, topic_search: int = 0, chunk_weight: float = 0.3, show_links: bool = False):
    ohtm_file = convert_ohtm_file(ohtm_file)
    anonymized_status = False
    if ohtm_file["settings"]["topic_modeling"]["trained"] == "True":
        sent_final = []
        link_tape = "1"
        for archive in ohtm_file["weight"]:
            for interview in ohtm_file["weight"][archive]:
                try:
                    if ohtm_file["corpus"][archive][interview]["anonymized"] == "True":
                        anonymized_status = True
                except KeyError:
                    anonymized_status = False
                for chunks in ohtm_file["weight"][archive][interview]:
                    chunk_start_marker = 0
                    speaker = "None"
                    if str(ohtm_file["weight"][archive][interview][chunks][str(topic_search)]) >= str(chunk_weight):
                        if "e" in str(ohtm_file["weight"][archive][interview][chunks][str(topic_search)]):
                            next
                        else:
                            sent_current = []
                            for number in ohtm_file["corpus"][archive][interview]["sent"]:
                                int_sent = copy.deepcopy(ohtm_file["corpus"][archive][interview]["sent"][number]["chunk"])
                                if int(int_sent) == int(chunks):
                                    chunk_start_marker += 1
                                    if chunk_start_marker == 1:  # to mark the beginning of the chunk for the first timecode
                                        if ohtm_file["corpus"][archive][interview]["sent"][number]["time"] != {}:
                                            timcodes_available = True
                                            chunk_start_time = \
                                            ohtm_file["corpus"][archive][interview]["sent"][number]["time"]
                                            link_tape = \
                                            ohtm_file["corpus"][archive][interview]["sent"][number]["tape"]
                                        else:
                                            timcodes_available = False
                                            link_tape = "1"
                                            chunk_start_time = "False"
                                    if ohtm_file["corpus"][archive][interview]["sent"][number]["speaker"] == {}:
                                        sent_current.append(str(ohtm_file["corpus"][archive][interview]["sent"][number]["raw"]) + " ")
                                        chunk_end_time = \
                                        ohtm_file["corpus"][archive][interview]["sent"][number]["time"]
                                    else:
                                        if speaker == ohtm_file["corpus"][archive][interview]["sent"][number]["speaker"]:
                                            sent_current.append(str(
                                                ohtm_file["corpus"][archive][interview]["sent"][number]["raw"]) + " ")
                                            chunk_end_time = \
                                                ohtm_file["corpus"][archive][interview]["sent"][number]["time"]
                                        else:
                                            sent_current.append(str("*" +
                                                ohtm_file["corpus"][archive][interview]["sent"][number]["speaker"]) + ":* ")
                                            sent_current.append(str(
                                                ohtm_file["corpus"][archive][interview]["sent"][number]["raw"]) + " ")
                                            speaker = ohtm_file["corpus"][archive][interview]["sent"][number]["speaker"]
                                            chunk_end_time = \
                                                ohtm_file["corpus"][archive][interview]["sent"][number]["time"]
                            sent_current = " ".join(sent_current)
                            sent_current_2 = (str(ohtm_file["weight"][archive][interview][chunks][str(topic_search)]),
                                              interview, chunks, sent_current, chunk_start_time, chunk_end_time,
                                              timcodes_available, link_tape, archive, anonymized_status
                                              )
                            sent_final.append(sent_current_2)
        print("\n" + "The Topic Nr. " + str(topic_search) + " above " + str(chunk_weight)
              + " was found in this chunks:")
        print("weight | interview-id | chunk | raw-text")
        sent_final.sort(reverse = True)
        for interview in sent_final:
            if interview[-1]:
                if interview[-4]:
                    link = create_link(interview[-2].lower(), interview[1].lower(), interview[4], interview[7])
                    print(interview[0] + " | " + interview[1] + " | " + interview[2] + " | " + interview[4] + "–"
                          + str(interview[5]) + " | " + "This interview is anonymized and can be found: " + link)
                else:
                    link = create_link(interview[-2].lower(), interview[1].lower(), interview[4], interview[7])
                    print(interview[0] + " | " + interview[1] + " | " + interview[2] + " | " + "no timecodes" + " | "
                          + "This interview is anonymized and can be found: " + link)
            else:
                if interview[-4]:
                    print(interview[0] + " | " + interview[1] + " | " + interview[2] + " | " + interview[4] + "–"
                          + str(interview[5]) + " | " + interview[3])
                else:
                    print(interview[0] + " | " + interview[1] + " | " + interview[2] + " | " + "no timecodes" + " | "
                          + interview[3])
                if show_links:
                    link = create_link(interview[-2].lower(), interview[1].lower(), interview[4], interview[7])
                    print(link)
        print("\n")
        print("To view one chunk in a better presentation,"
              " print the chunk you want directly with 'print_interview_chunk'.")
    else:
        print("No Topic Model trained")


def print_chunk_with_interview_weight_search(ohtm_file, interview_id: str = "", topic_search: int = 0,
                                             chunk_weight: float = 0.3, show_links: bool = False):
    ohtm_file = convert_ohtm_file(ohtm_file)
    anonymized_status = False
    if ohtm_file["settings"]["topic_modeling"]["trained"] == "True":
        for archive in ohtm_file["weight"]:
            if interview_id in ohtm_file["weight"][archive]:
                try:
                    if ohtm_file["corpus"][archive][interview_id]["anonymized"] == "True":
                        anonymized_status = True
                except KeyError:
                    anonymized_status = False
                sent_final = []
                for chunks in ohtm_file["weight"][archive][interview_id]:
                    speaker = "None"
                    if str(ohtm_file["weight"][archive][interview_id][chunks][str(topic_search)]) >= str(chunk_weight):
                        if "e" in str(ohtm_file["weight"][archive][interview_id][chunks][str(topic_search)]):
                            next
                        else:
                            sent_current = []
                            chunk_start_marker = 0
                            for sent in ohtm_file["corpus"][archive][interview_id]["sent"]:
                                int_sent = copy.deepcopy(
                                    ohtm_file["corpus"][archive][interview_id]["sent"][sent]["chunk"])
                                if int(int_sent) == int(chunks):
                                    chunk_start_marker += 1
                                    if chunk_start_marker == 1:  # to mark the beginning of the chunk for the first timecode
                                        if ohtm_file["corpus"][archive][interview_id]["sent"][sent]["time"] != {}:
                                            timcodes_available = True
                                            chunk_start_time = \
                                            ohtm_file["corpus"][archive][interview_id]["sent"][sent]["time"]
                                            link_tape = \
                                            ohtm_file["corpus"][archive][interview_id]["sent"][sent]["tape"]
                                        else:
                                            timcodes_available = False
                                            link_tape = "1"
                                            chunk_start_time = "False"
                                    if ohtm_file["corpus"][archive][interview_id]["sent"][sent]["speaker"] == {}:
                                        sent_current.append(str(ohtm_file["corpus"][archive][interview_id]["sent"][sent]["raw"]) + "")
                                        chunk_end_time = \
                                        ohtm_file["corpus"][archive][interview_id]["sent"][sent]["time"]
                                    else:
                                        if speaker == ohtm_file["corpus"][archive][interview_id]["sent"][sent]["speaker"]:
                                            sent_current.append(str(
                                                ohtm_file["corpus"][archive][interview_id]["sent"][sent]["raw"]) + "")
                                            chunk_end_time = \
                                                ohtm_file["corpus"][archive][interview_id]["sent"][sent]["time"]
                                        else:
                                            sent_current.append(str("*" +
                                                ohtm_file["corpus"][archive][interview_id]["sent"][sent]["speaker"]) + ":* ")
                                            sent_current.append(str(
                                                ohtm_file["corpus"][archive][interview_id]["sent"][sent]["raw"]) + "")
                                            speaker = ohtm_file["corpus"][archive][interview_id]["sent"][sent]["speaker"]
                                            chunk_end_time = \
                                                ohtm_file["corpus"][archive][interview_id]["sent"][sent]["time"]
                            sent_current = " ".join(sent_current)
                            sent_current_2 = (
                                str(ohtm_file["weight"][archive][interview_id][chunks][str(topic_search)]),
                                interview_id, chunks, sent_current, chunk_start_time, chunk_end_time,
                                timcodes_available, link_tape, archive
                            )
                            sent_final.append(sent_current_2)
                if not sent_final:
                    print("\n" + "No chunk with the topic nr. "+str(topic_search)+
                          " with a weight above " + str(chunk_weight) + " was found in " + str(interview_id)+".")
                else:
                    print("\n" + "The topic nr. " +
                          str(topic_search) + " was found in " + str(interview_id) + " within this chunks:")
                    print("weight | interview-id | chunk | timecode | raw-text")
                    for sent in sent_final:
                        if anonymized_status:
                            if sent[-3]:
                                link = create_link(sent[-1].lower(), sent[1].lower(), sent[4],
                                                   sent[7])
                                print(sent[0] + " | " + sent[1] + " | " + sent[2] + " | " + sent[
                                    4] + "–"
                                      + str(
                                    sent[5]) + " | " + "This interview is anonymized and can be found: " + link)
                            else:
                                link = create_link(sent[-1].lower(), sent[1].lower(), sent[4],
                                                   sent[7])
                                print(sent[0] + " | " + sent[1] + " | " + sent[
                                    2] + " | " + "no timecodes" + " | "
                                      + "This interview is anonymized and can be found: " + link)
                        else:
                            if sent[-3]:
                                print(sent[0] + " | " + sent[1] + " | " + sent[2] + " | " + sent[4] + "–"
                                      + str(sent[5]) + " | " + sent[3])
                            else:
                                print(sent[0] + " | " + sent[1] + " | " + sent[2] + " | " + "no timecodes"
                                      + " | " + sent[3])
                            if show_links:
                                link = create_link(sent[-1].lower(), sent[1].lower(), sent[4], sent[7])
                                print(link)
                    print("\n")
                    print(
                        "To view one chunk in a better presentation, print the chunk you want directly with 'print_interview_chunk'.")
    else:
        print("No Topic Model trained")

