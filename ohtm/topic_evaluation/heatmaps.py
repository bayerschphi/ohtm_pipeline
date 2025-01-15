from builtins import print
import json
import pandas as pd
import plotly_express as px


def heatmap_corpus(top_dic, option_selected: str = "all",
                   show_fig: bool = True, return_fig: bool = False, z_score: bool = True):

    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic

    if top_dic["settings"]["topic_modeling"]["trained"] == "True":
        heat_dic = {}
        for archive in top_dic["weight"]:
            for interview in top_dic["weight"][archive]:
                heat_dic[interview] = {}
                count = 0
                for c in top_dic["weight"][archive][interview]:
                    count += 1
                    for t in top_dic["weight"][archive][interview][c]:
                        if t not in heat_dic[interview]:
                            heat_dic[interview].update({t: top_dic["weight"][archive][interview][c][t]})
                        else:
                            heat_dic[interview].update(
                                {t: heat_dic[interview][t] + top_dic["weight"][archive][interview][c][t]})
                for entry in heat_dic[interview]:
                    heat_dic[interview].update({entry:heat_dic[interview][entry] / count})

        if option_selected == "all":
            df = pd.DataFrame.from_dict(heat_dic)

        else:
            dff = {}
            for i in heat_dic:
                if i[:3] == option_selected:
                    dff[i] = heat_dic[i]
            df = pd.DataFrame.from_dict(dff)

        # Berechnung der z-Standardisierung
        if z_score :
            mean = df.mean()
            std_dev = df.std()
            z_scores = ((df - mean)/std_dev)
            df = z_scores

        df = df.swapaxes("index", "columns")
        fig = px.imshow(df, color_continuous_scale='dense', aspect='auto')
        fig.update_traces(hovertemplate="Interview: %{y}" "<br>Topic: %{x}" "<br>Weight: %{z}<extra></extra>")
        fig.update_layout(clickmode='event+select')
        fig.update_layout(clickmode='event+select')
        fig.update(layout_coloraxis_showscale=False)
        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        if show_fig:
            fig.show()
        if return_fig:
            return fig
    else:
        print("No Topic Model trained")


def heatmap_interview(top_dic, interview_id: str = "",  show_fig: bool = True, return_fig: bool = False):

    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic

    if top_dic["settings"]["topic_modeling"]["trained"] == "True":
        dff = {}
        for chunks in top_dic["weight"][interview_id[0:3]][interview_id]:
            dff[chunks] = top_dic["weight"][interview_id[0:3]][interview_id][chunks]

        df = pd.DataFrame.from_dict(dff)
        df.index = pd.to_numeric(df.index)

        # Berechnung der z-Standardisierung
        mean = df.mean()
        std_dev = df.std()
        z_scores = ((df - mean)/std_dev)

        titel = "Heatmap Interview: " + interview_id
        fig = px.imshow(df, color_continuous_scale='deep')
        fig.update_traces(hovertemplate="Chunk: %{x}" "<br>Topic: %{y}" "<br>Weight: %{z}<extra></extra>")
        if show_fig:
            fig.show()
        if return_fig:
            return fig

    else:
        print("No Topic Model trained")


