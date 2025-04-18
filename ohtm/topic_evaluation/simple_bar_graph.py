import json
import pandas as pd
import plotly_express as px
from ohtm.basic_functions.convert_ohtm_file import convert_ohtm_file


def bar_graph_corpus(ohtm_file, show_fig: bool = True, return_fig: bool = False):

    ohtm_file = convert_ohtm_file(ohtm_file)

    if ohtm_file["settings"]["topic_modeling"]["trained"] == "True":
        interview_dic = {}
        for archive in ohtm_file["weight"]:
            if archive not in interview_dic:
                interview_dic[archive] = {}
            for interview in ohtm_file["weight"][archive]:
                interview_dic[archive][interview] = {}
                count = 0
                for c in ohtm_file["weight"][archive][interview]:
                    count += 1
                    for t in ohtm_file["weight"][archive][interview][c]:
                        if t not in interview_dic[archive][interview]:
                            interview_dic[archive][interview].update(
                                {t: ohtm_file["weight"][archive][interview][c][t]})
                            # das int(t) muss genutzt werden, da das speichern in Store die Datei umwandelt
                        else:
                            interview_dic[archive][interview].update(
                                {t: interview_dic[archive][interview][t] + ohtm_file["weight"][archive][interview][c][t]})
                for entry in interview_dic[archive][interview]: (interview_dic[archive][interview].update({entry: interview_dic[archive][interview][entry] / count}))

        bar_dic = {}
        for archive in interview_dic:
            bar_dic[archive] = {}
            count = 0
            for interview in interview_dic[archive]:
                count += 1
                for t in interview_dic[archive][interview]:
                    if t not in bar_dic[archive]:
                        bar_dic[archive].update({t: interview_dic[archive][interview][t]})
                    else:
                        bar_dic[archive].update({t: bar_dic[archive][t] + interview_dic[archive][interview][t]})
            for entry in bar_dic[archive]:
                bar_dic[archive].update({entry: bar_dic[archive][entry] / count})

        print(bar_dic)
        bar_dic_simple = {}

        for archive in bar_dic:
            for topic in bar_dic[archive]:
                if topic not in bar_dic_simple:
                    bar_dic_simple.update({topic:bar_dic[archive][topic]})
                else:
                    bar_dic_simple.update({topic: bar_dic_simple[topic] + bar_dic[archive][topic]})


        bar_dic_simple_final = []
        for topic in bar_dic_simple:
            bar_dic_simple_final.append((topic, bar_dic_simple[topic]))

        print(bar_dic_simple)

        df = pd.DataFrame(bar_dic_simple, index=[0])
        # df = pd.DataFrame(bar_dic_simple_final)

        # Min-Max-Normalisierung: Skalieren Sie die Daten auf den Wertebereich [0, 1]
        # min_val = df.min()
        # max_val = df.max()
        # normalized_data = (df - min_val) / (max_val - min_val)
        # df = normalized_data

        # df.index = pd.to_numeric(df.index)
        print(df)
        fig = px.bar(df.T, color_discrete_sequence=px.colors.qualitative.G10)
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), title_text="OHD_final_100C_90T_A5")
        if show_fig:
            fig.show()
        if return_fig:
            return fig
    else:
        print("No Topic Model trained")
