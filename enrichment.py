import os
import csv
import json



'''
Das muss ins jSon
'''

topic_labels = {
    0: "Umbruch / Transformation",
    1: "Arbeit / Industrie",
    2: "Arbeit / Bau",
    3: "Stahlindustrie / Ruhrgebiet",
    4: "Arbeitsmigration",
    5: "Justiz",
    6: "Judentum",
    7: "Kleidung / Mode",
    8: "Erziehung (auch: Erziehungseinrichtungen)",
    9: "Krieg (Häufig WK II / Ostfront)",
    10: "Natur",
    11: "Politische Jugendorganisationen / DDR",
    12: "Judenverfolgung / Deportation",
    13: "Colonia Dignidad / Strukturen",
    14: "Haushalt / Hausarbeit",
    15: "Urlaub / Reisen",
    16: "Krankheit / Medizinische Versorgung",
    17: "Familie / Familienleben / Kernfamilie",
    18: "Innerdeutsche Grenze / Zwangsumsiedlung / ländlicher Raum",
    19: "Empfindungen (Häufig: positive E.)",
    20: "Versorgung",
    21: "Naturschutz",
    22: "Arbeit / Bergbau",
    23: "Interessenverbände / Gremien",
    24: "Paratext",
    25: "Genussmittel",
    26: "Landwirtschaft / Bauernhof",
    27: "Familie / Schicksalsschlag / Verlust",
    28: "Ausbildung",
    29: "Bauen / Wohnen",
    30: "Parteien / Politik",
    31: "Colonia Dignidad / Alltag",
    32: "Bahnfahren / Transport",
    33: "Universität",
    34: "Judentum / Südosteuropa / Zwangsarbeit",
    35: "Orte / NRW",
    36: "Familie / Krieg / Osteuropa",
    37: "Feiern / Festtage",
    38: "Christentum",
    39: "NS / Organisationen",
    40: "Paratext",
    41: "WK II / Zwangsarbeit",
    42: "Neuapostolische Kirche / Sekten",
    43: "Empfindungen",
    44: "Migration / Sprache",
    45: "Finanzen",
    46: "Erinnerung / Erinnerungskultur",
    47: "Ruhrgebiet",
    48: "Sucht",
    49: "Mobilität / Fahrzeuge",
    50: "Arbeit (auch: Einstellung zu A.)",
    51: "Subkultur",
    52: "Lager / Sowjetische Speziallager",
    53: "WK II / Lager",
    54: "Studium",
    55: "Bombenkrieg / WK II",
    56: "Krieg (Häufig: WK II / Front)",
    57: "Arbeit / Stahlindustrie / DDR",
    58: "Systemvergleich / Systemwechsel",
    59: "Länder / Nationen",
    60: "Literatur / Printmedien",
    61: "Rundfunk / Fernsehen",
    62: "Israel",
    63: "Familie / Heirat / Geburt",
    64: "Arbeit / Wirtschaft / DDR",
    65: "Familie",
    67: "Gewerkschaft / Betriebsrat",
    68: "Lebensmittel / Ernährung",
    69: "WK II / Lager",
    70: "Sport / Freizeit / Vereinswesen",
    72: "Fotografie / Bildende Kunst",
    73: "Interviewsituation",
    74: "Empfindungen / Erinnern",
    75: "Lebenslauf",
    76: "Soziale Bewegungen",
    77: "Wohnung / Wohnen",
    78: "Printmedien",
    79: "WK II / Lager / Kriegsgefangenschaft",
    80: "Film / Fernsehen",
    81: "Politische Haft / SBZ / DDR",
    82: "Militär",
    83: "WKII / Kriegsende / Alliierte",
    84: "Industrie / Wirtschaft",
    85: "Flucht / Vertreibung",
    86: "Tagesrhythmus",
    87: "Soziale Kontakte / Freizeit",
    88: "Familie / Verwandtschaft / Vorfahren",
    89: "Bürokratie",
    90: "Gewalt / Repression",
    91: "Kriegsende / Nachkriegszeit",
    93: "Reflexion",
    94: "Vergangenheit / Verarbeitung",
    95: "Schule",
    96: "Frauen in NS-Organisationen",
    97: "Erschwerte Lebensbedingungen",
    98: "Bühne / Musik / Schauspiel",
    99: "Osteuropa / Österreich-Ungarn"

}
registry_ids = {
    0: 90443630,
    1: 90443665,
    2: 90443666,
    3: 90443672,
    4: 90443675,
    5: 90443679,
    6: 90443682,
    7: 90443738,
    8: 90443748,
    9: 90443772,
    10: 90443702,
    11: 90443654,
    12: 90443709,
    13: 90443685,
    14: 90443688,
    15: 90443719,
    16: 90443723,
    17: 90443689,
    18: 90443655,
    19: 90443726,
    20: 90443757,
    21: 90443705,
    22: 90443667,
    23: 90443706,
    24: 90443733,
    25: 90443739,
    26: 90443703,
    27: 90443690,
    28: 90443749,
    29: 90443740,
    30: 90443680,
    31: 90443686,
    32: 90443778,
    33: 90443750,
    34: 90443710,
    35: 90443660,
    36: 90443711,
    37: 90443741,
    38: 90443683,
    39: 90443780,
    40: 90443734,
    41: 90443712,
    42: 90443684,
    43: 90443727,
    44: 90443676,
    45: 90443758,
    46: 90443760,
    47: 90443661,
    48: 90443724,
    49: 90443779,
    50: 90443668,
    51: 90443761,
    52: 90443713,
    53: 90443714,
    54: 90443751,
    55: 90443773,
    56: 90443774,
    57: 90443669,
    58: 90443656,
    59: 90443662,
    60: 90443762,
    61: 90443763,
    62: 90443781,
    63: 90443691,
    64: 90443657,
    65: 90443692,
    67: 90443670,
    68: 90443742,
    69: 90443715,
    70: 90443720,
    72: 90443764,
    73: 90443735,
    74: 90443728,
    75: 90443736,
    76: 90443707,
    77: 90443743,
    78: 90443765,
    79: 90443716,
    80: 90443766,
    81: 90443717,
    82: 90443775,
    83: 90443776,
    84: 90443673,
    85: 90443677,
    86: 90443744,
    87: 90443721,
    88: 90443693,
    89: 90443745,
    90: 90443729,
    91: 90443658,
    93: 90443730,
    94: 90443731,
    95: 90443752,
    96: 90443777,
    97: 90443746,
    98: 90443767,
    99: 90443663
}

topic_cluster = {}
stoplist = ['66', '71', '92']# verrasuchte topics
working_folder = "C:\\Users\\moebusd\\sciebo\\OHD\\Data TM OHD\\"
enrichment_input = "C:\\Users\\moebusd\\sciebo\\OHD\\Data TM OHD\\enrichment input\\"
enrichment_output = "C:\\Users\\moebusd\\sciebo\\OHD\\Data TM OHD\\enrichment output\\"
load_file_name = "OHD_final_100C_100T_A5"

with open(working_folder + load_file_name) as f:
    top_dic = json.load(f)

def enrichment(enrichment_input, enrichment_output, human_readable = True, registry = True):
    counter_tag = 0
    counter_line = 0
    for file in os.listdir(enrichment_input): # Erscfhließungstabele OHD einlesen
        with open(enrichment_input + file, 'r', newline='', encoding='utf-8') as csvfile:
            interview = list(csv.reader(csvfile, delimiter="\t", quotechar=None))
            #print(interview)
            interview_id = file.split(".")[0].split("_")[0].upper() # Interview Id aus Namen der erschließúngstabelle entnehmen
            print(interview_id)
            chunk_set = 0
            topics = []
            for top in top_dic["weight"][interview_id[0:3]][interview_id][str(chunk_set)]:                             # topic labels/ids for Chunk 0
                topics.append((top_dic["weight"][interview_id[0:3]][interview_id][str(chunk_set)][top], str(top))) # für jedes Topic Übergabe Weight/T-Nr.
            top_tops_sorted = sorted(topics, reverse=True)[:3] # die drei gewichtigsten Topics absteigend sortiert
            if human_readable: # Label wird einfach eingetragen
                top_tops = [topic_labels[int(top[1])] for top in top_tops_sorted if top not in stoplist and top[0] >= 0.1]

            if registry: # Register-IDs aus OHD, die importiert werden können
                top_tops_registry = [registry_ids[int(top[1])] for top in top_tops_sorted if top not in stoplist and top[0] >= 0.1]

            for nr_line, line in enumerate(interview):
                if line[1][:8] == top_dic["corpus"][interview_id[0:3]][interview_id]["sent"]['1']["time"][:8]:                    # labels/ids in Tabelle eintragen, wenn TC matcht
                    if line[9] == '': #falls noch keine registerverknüpfungen vorhanden sind
                        transfer = [line[0], line[1], line[2], line[3], line[4], str(top_tops).replace("'", "").replace("[", "| ").replace("]", " |").replace(",", " |"), line[6], line[7], line[8], str(top_tops_registry).replace('[', '').replace(']', '').replace(', ', '#'), line[10], line[11]]
                    else: #falls schon registerverknüpfungen vorhanden sind
                        transfer = [line[0], line[1], line[2], line[3], line[4], str(top_tops).replace("'", "").replace("[", "| ").replace("]", " |").replace(",", " |"), line[6], line[7], line[8], line[9] + '#' + str(top_tops_registry).replace('[', '').replace(']', '').replace(', ', '#'), line[10], line[11]]

                    interview.pop(nr_line)
                    interview.insert(nr_line, transfer)
                    chunk_set += 1
                    topics = []
                    break

            for sents in top_dic["corpus"][interview_id[0:3]][interview_id]["sent"]:

                if top_dic["corpus"][interview_id[0:3]][interview_id]["sent"][sents]["chunk"] != chunk_set:
                    continue
                if top_dic["corpus"][interview_id[0:3]][interview_id]["sent"][sents]["chunk"] == chunk_set:
                    try:
                        for top in top_dic["weight"][interview_id[0:3]][interview_id][str(chunk_set)]:  # topic labels/ids for Chunk 0
                            topics.append((top_dic["weight"][interview_id[0:3]][interview_id][str(chunk_set)][top],
                                         str(top)))                                                     # für jedes Topic Übergabe Weight/T-Nr.
                        top_tops_sorted = sorted(topics, reverse=True)[:3]                              # die drei gewichtigsten Topics absteigend sortiert
                        if human_readable:                                                              # Label wird einfach eingetragen
                            top_tops = [(topic_labels[int(top[1])]) for top in top_tops_sorted if top not in stoplist and top[0] >= 0.1]

                        if registry:  # Register-IDs aus OHD, die importiert werden können
                            top_tops_registry = [registry_ids[int(top[1])] for top in top_tops_sorted if top not in stoplist and top[0] >= 0.1]

                        for nr_line, line in enumerate(interview):
                            if line[1][:8] == top_dic["corpus"][interview_id[0:3]][interview_id]["sent"][sents]["time"][:8] and line[0] == top_dic["corpus"][interview_id[0:3]][interview_id]["sent"][sents]["tape"]:  # labels/ids in Tabelle eintragen, wenn TC matcht
                                if line[9] == '': # falls noch keine registerverknüpfungen vorhanden sind
                                    transfer = [line[0], line[1], line[2], line[3], line[4], str(top_tops).replace("'", "").replace("[", "| ").replace("]", " |").replace(",", " |"), line[6], line[7], line[8], str(top_tops_registry).replace('[', '').replace(']', '').replace(', ', '#'), line[10], line[11]]
                                else: #falls registerverknüpfungen vorhanden sind
                                    transfer = [line[0], line[1], line[2], line[3], line[4], str(top_tops).replace("'", "").replace("[", "| ").replace("]", " |").replace(",", " |"), line[6], line[7], line[8], line[9] + '#'+str(top_tops_registry).replace('[', '').replace(']', '').replace(', ', '#'), line[10], line[11]]
                                interview.pop(nr_line)
                                interview.insert(nr_line, transfer)
                                topics = []
                                break
                        chunk_set += 1
                    except KeyError:
                        continue
        with open(enrichment_output + file.split('.')[0] + 'enriched.csv', 'w', encoding='UTF-8', newline = '') as myfile:
            wr = csv.writer(myfile, delimiter="\t", quotechar=None)
            wr.writerows(interview)


enrichment(enrichment_input, enrichment_output)