from builtins import print
import pandas as pd
import plotly_express as px
from ohtm_pipeline.basic_functions.convert_ohtm_file import convert_ohtm_file
import numpy as np
import ast


def heatmap_corpus(ohtm_file, option_selected: str = "all",
                   show_fig: bool = True, return_fig: bool = False, z_score: bool = True):

    ohtm_file = convert_ohtm_file(ohtm_file)

    if ohtm_file["settings"]["topic_modeling"]["trained"] == "True":
        if option_selected == "all":
            heat_dic = {}
            for archive in ohtm_file["weight"]:
                for interview in ohtm_file["weight"][archive]:
                    heat_dic[interview] = {}
                    count = 0
                    for c in ohtm_file["weight"][archive][interview]:
                        count += 1
                        for t in ohtm_file["weight"][archive][interview][c]:
                            if t not in heat_dic[interview]:
                                heat_dic[interview].update({t: ohtm_file["weight"][archive][interview][c][t]})
                            else:
                                heat_dic[interview].update(
                                    {t: heat_dic[interview][t] + ohtm_file["weight"][archive][interview][c][t]})
                    for entry in heat_dic[interview]:
                        heat_dic[interview].update({entry: heat_dic[interview][entry] / count})
            df = pd.DataFrame.from_dict(heat_dic)
        else:
            archive = option_selected
            heat_dic = {}
            for interview in ohtm_file["weight"][archive]:
                heat_dic[interview] = {}
                count = 0
                for c in ohtm_file["weight"][archive][interview]:
                    count += 1
                    for t in ohtm_file["weight"][archive][interview][c]:
                        if t not in heat_dic[interview]:
                            heat_dic[interview].update({t: ohtm_file["weight"][archive][interview][c][t]})
                        else:
                            heat_dic[interview].update(
                                {t: heat_dic[interview][t] + ohtm_file["weight"][archive][interview][c][t]})
                for entry in heat_dic[interview]:
                    heat_dic[interview].update({entry: heat_dic[interview][entry] / count})

            df = pd.DataFrame.from_dict(heat_dic)

        if z_score:
            mean = df.mean()
            std_dev = df.std()
            z_scores = ((df - mean) / std_dev)
            df = z_scores

        df = df.transpose()
        
        # # DataFrame mit 3 Rows und 6 Columns ("0"–"5")

        # groups = ohtm_file["topic_labels"]["clusters"]

        # grouped = pd.DataFrame({
        #     key: df[[str(c) for c in (cols if isinstance(cols, list) else ast.literal_eval(cols))]].sum(axis=1)
        #     for key, (_, cols) in groups.items()
        # })


        # # Labels extra abspeichern (z. B. für Plotly hovertext)
        # labels = {key: label for key, (label, _) in groups.items()}


        # print(grouped)

        # df = grouped 
            

        # fig = px.imshow(df, color_continuous_scale='dense', aspect='auto', labels=dict(x="Group", y="Sample", color="Sum"))
        fig = px.imshow(df, color_continuous_scale='dense', aspect='auto')
        fig.update_traces(hovertemplate="Interview: %{y}" "<br>Topic: %{x}" "<br>Weight: %{z}<extra></extra>")
        fig.update_layout(clickmode='event+select')
        fig.update_layout(clickmode='event+select')
        fig.update(layout_coloraxis_showscale=False)

        fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
        # hover_text = [
        #     [labels[str(col)] for col in grouped.columns]  # Labels pro Column
        #     for _ in grouped.index
        # ]

        # fig.update_traces(
        #     text=hover_text,
        #     hovertemplate="Interview: %{y}<br>Cluster: %{x}<br>Label: %{text}<br>Value: %{z}<extra></extra>"
        #     )


        # label_dict = ohtm_file["topic_labels"]["labels"] 
        # x_labels = [label_dict[c] for c in df.columns] 
        # customdata = np.tile(x_labels, (len(df.index), 1))

        # # customdata und Hovertemplate setzen
        # fig.data[0].update(
        #     customdata=customdata,
        #     hovertemplate="Variable: %{y}<br>X-Label: %{customdata}<br>Wert: %{z}<extra></extra>"
        # )
        fig.update_layout(
                xaxis_title="Topics",
                yaxis_title="Interviews", 
            )
        if show_fig:
            fig.show()
        if return_fig:
            return fig

    else:
        print("No Topic Model trained")


"""
This function has to be tested in the dash. Because now it is really slow. With the chagen to possilbe different 
archive namens than the first 3 letters of the interview id, i had to find another way. Maye this function has to be
improved. (17.1.2025)
"""


def heatmap_interview(ohtm_file, interview_id: str = "", show_fig: bool = True, return_fig: bool = False):

    ohtm_file = convert_ohtm_file(ohtm_file)
    if ohtm_file["settings"]["topic_modeling"]["trained"] == "True":
        dff = {}
        for archive in ohtm_file["weight"]:
            if interview_id in ohtm_file["weight"][archive]:
                for chunks in ohtm_file["weight"][archive][interview_id]:
                    dff[chunks] = ohtm_file["weight"][archive][interview_id][chunks]

        df = pd.DataFrame.from_dict(dff)
        df.index = pd.to_numeric(df.index)

        # Berechnung der z-Standardisierung
        mean = df.mean()
        std_dev = df.std()
        z_scores = ((df - mean)/std_dev)

        titel = "Heatmap Interview: " + interview_id
        fig = px.imshow(df, color_continuous_scale='dense')
        fig.update_traces(hovertemplate="Chunk: %{x}" "<br>Topic: %{y}" "<br>Weight: %{z}<extra></extra>")
        fig.update(layout_coloraxis_showscale=False)
        fig.update_layout(
                xaxis_title="Chunks",
                yaxis_title="Topics",
                title = "Interviewheatmap " + interview_id
            )
        
        if show_fig:
            fig.show()
        if return_fig:
            return fig

    else:
        print("No Topic Model trained")
