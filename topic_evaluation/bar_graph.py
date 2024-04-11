import json
import pandas as pd
import plotly_express as px

def bar_graph_corpus(top_dic, show_fig: bool = True, return_fig: bool = False):

    bar_dic = {}
    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic

    if top_dic["settings"]["topic_modeling"]["trained"] == "True":

        for archive in top_dic["weight"]:
            bar_dic[archive] = {}
            count = 0
            for interview in top_dic["weight"][archive]:
                count += 1
                for chunk in top_dic["weight"][archive][interview]:
                    for t in top_dic["weight"][archive][interview][chunk]:
                        if t not in bar_dic[archive]:
                            bar_dic[archive].update({t: top_dic["weight"][archive][interview][chunk][t]})
                        else:
                            bar_dic[archive].update({t: bar_dic[archive][t] + top_dic["weight"][archive][interview][chunk][t]})
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
