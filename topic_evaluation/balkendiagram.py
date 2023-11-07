from main_pipeline.main_settings import *
import json

with open("C:\\Users\\phili\\FAUbox\\Oral History Digital\\Topic Modeling\\main test\\ADG_complete_test\\heatmap_test_80_chunks_30_topics", "rb") as f:
    top_dic = json.load(f)


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

fig = px.bar(df, color_discrete_sequence=px.colors.qualitative.G10)
fig.show()