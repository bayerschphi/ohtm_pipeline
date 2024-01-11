from builtins import print
import json
import pandas as pd
import plotly_express as px

def heatmap_corpus(top_dic, option_selected: str = "all", show_fig: bool = True, return_fig: bool = False):

    heat_dic = {}
    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic

    for archive in top_dic["weight"]:
        for i in top_dic["weight"][archive]:
            heat_dic[i] = {}
            count = 0
            for c in top_dic["weight"][archive][i]:
                count += 1
                for t in top_dic["weight"][archive][i][c]:
                    if t not in heat_dic[i]:
                        heat_dic[i].update({t: top_dic["weight"][archive][i][c][t]})  # das int(t) muss genutzt werden, da das speichern in Store die Datei umwandelt
                    else:
                        heat_dic[i].update({t: heat_dic[i][t] + top_dic["weight"][archive][i][c][t]})
            for entry in heat_dic[i]:
                heat_dic[i].update({entry:heat_dic[i][entry] / count})

    df = pd.DataFrame.from_dict(heat_dic)

    # Berechnung der z-Standardisierung
    mean=df.mean()
    std_dev = df.std()
    z_scores = ((df - mean)/std_dev)

    if option_selected != "all":
        columns_to_extract = []
        for i in z_scores:
            if i[0:3] == option_selected:
                columns_to_extract.append(i)

        z_scores = z_scores[columns_to_extract]

    z_scores= z_scores.swapaxes("index", "columns")
    fig = px.imshow(z_scores, color_continuous_scale='deep', aspect='auto')
    fig.update_traces(hovertemplate="Interview: %{y}" "<br>Topic: %{x}" "<br>Weight: %{z}<extra></extra>")
    fig.update_layout(clickmode='event+select')
    fig.update_layout(clickmode='event+select')
    if show_fig == True:
        fig.show()
    if return_fig == True:
        return fig