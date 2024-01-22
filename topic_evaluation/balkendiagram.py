import json
import pandas as pd
import plotly.express as px

def bar_dic(top_dic, show_fig: bool = True, return_fig: bool = False):

    bar_dic = {}
    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic

    for a in top_dic["weight"]:
        bar_dic[a] = {}
        count = 0
        for i in top_dic["weight"][a]:
            count += 1
            for c in top_dic["weight"][a][i]:
                for t in top_dic["weight"][a][i][c]:
                    if t not in bar_dic[a]:
                        bar_dic[a].update({t: top_dic["weight"][a][i][c][t]})
                    else:
                        bar_dic[a].update({t: bar_dic[a][t] + top_dic["weight"][a][i][c][t]})
        for entry in bar_dic[a]:
            bar_dic[a].update({entry: bar_dic[a][entry] / count})

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