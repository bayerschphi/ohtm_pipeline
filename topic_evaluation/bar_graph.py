import json
import pandas as pd
import plotly_express as px

def bar_graph_corpus(top_dic, show_fig: bool = True, return_fig: bool = False):


    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic

    if top_dic["settings"]["topic_modeling"]["trained"] == "True":
        interview_dic = {}
        for archive in top_dic["weight"]:
            if archive not in interview_dic:
                interview_dic[archive] = {}
            for interview in top_dic["weight"][archive]:
                interview_dic[archive][interview] = {}
                count = 0
                for c in top_dic["weight"][archive][interview]:
                    count += 1
                    for t in top_dic["weight"][archive][interview][c]:
                        if t not in interview_dic[archive][interview]:
                            interview_dic[archive][interview].update({t: top_dic["weight"][archive][interview][c][t]})  # das int(t) muss genutzt werden, da das speichern in Store die Datei umwandelt
                        else:
                            interview_dic[archive][interview].update({t: interview_dic[archive][interview][t] + top_dic["weight"][archive][interview][c][t]})
                for entry in interview_dic[archive][interview]:
                     interview_dic[archive][interview].update({entry:interview_dic[archive][interview][entry] / count})

        print(interview_dic)
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



        df = pd.DataFrame.from_dict(bar_dic)

        # Min-Max-Normalisierung: Skalieren Sie die Daten auf den Wertebereich [0, 1]
        min_val = df.min()
        max_val = df.max()
        normalized_data = (df - min_val) / (max_val - min_val)
        df.index = pd.to_numeric(df.index)

        fig = px.bar(df, color_discrete_sequence=px.colors.qualitative.G10)
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        if show_fig == True:
            fig.show()
        if return_fig == True:
            return fig
    else:
        print("No Topic Model trained")
