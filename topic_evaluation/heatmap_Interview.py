import json
import pandas as pd
import plotly_express as px

def heatmap_interview(top_dic, interview_id: str = "ZWA060",  show_fig: bool = True, return_fig: bool = False):

    if type(top_dic) is not dict:
        top_dic = json.loads(top_dic)
    else:
        top_dic = top_dic
    dff = {}
    for chunks in top_dic["weight"][interview_id[0:3]][interview_id]:
        dff[chunks] = top_dic["weight"][interview_id[0:3]][interview_id][chunks]

    df = pd.DataFrame.from_dict(dff)
    df.index = pd.to_numeric(df.index)

    # Berechnung der z-Standardisierung
    mean=df.mean()
    std_dev = df.std()
    z_scores = ((df - mean)/std_dev)


    titel = "Heatmap Interview: " + interview_id
    fig = px.imshow(df, color_continuous_scale='deep')
    fig.update_traces(hovertemplate="Chunk: %{x}" "<br>Topic: %{y}" "<br>Weight: %{z}<extra></extra>")
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20))
    if show_fig == True:
        fig.show()
    if return_fig == True:
        return fig