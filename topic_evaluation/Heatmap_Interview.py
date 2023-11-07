from main_pipeline.main_settings import *

with open("C:\\Users\\phili\\FAUbox\\Oral History Digital\\Topic Modeling\\main test\\ADG_complete_test\\heatmap_test_80_chunks_30_topics", "rb") as f:
    top_dic = json.load(f)


if type(top_dic) is not dict:
    top_dic = json.loads(top_dic)
else:
    top_dic = top_dic
interview_id = "ZWA060"
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
fig.show()