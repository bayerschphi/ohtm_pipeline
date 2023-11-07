def keyword_diversity(top_words, number_of_words):
    '''
     Hier soll die Einzigartigkeit von Keywords innerhalb der Topics untersucht
     werden, in je weniger Topics ein Wort enthalten ist, desto trennschärfer
     sollten die Topics sein. Vgl. mit der Relevance Metric bei pyLDAvis,
     nähere Infos dazu im oben verlinkten Paper, und dem Exclusivity Score
     im Paper von Thompson/Mimno. Bislang harter Filter, es werden NUR
     einzigartige Wörter gezählt, ich möchte einen Threshold einbauen,
     dass "seltene" Wörter besser bewertet werden, also beispielsweise
     auch Wörter, die in 2-3 Topics vorkommen einen guten Score bekommen,
     Wörter, die in allen Topics vorkommen, einen schlechten. Das könnte
     man dann auch noch mit der jeweiligen Gewichtung im Topic verrechnen.
     Für Dennis hilfreich, weil er möglichst trennscharfe und konsistente
     Topics braucht, um die pluralistischen Inhalte der Sammlung abzubilden.
     -> evtl. noch in Zusammenhang mit Dictionary bringen
     '''

    import re
    top_words_combined = []
    for line in top_words:
        top_words_combined.append(line[1].split(' + ')[:number_of_words])
    top_words = re.findall(r"\"(.*?)\"", str(top_words_combined))

    print(len(top_words))
    print(len(set(top_words)))
    singularity = (len(set(top_words)) / (int(len(top_words)))*100)# * number_of_words)) * 100
    print(str(int(singularity)) + '%')


def topic_search(topic_number, doc_tops, raw_data, average_topic_weight, *threshold_custom_value):
     '''
     if threshold_custom_value is left empty, average topic weight is set as threshold
     treshold_custom_value must be float in range 0.0 and 1.0
     '''

     if threshold_custom_value:
             threshold_topic_weight = threshold_custom_value
     else:
             threshold_topic_weight = average_topic_weight


     for j, line in enumerate(doc_tops):
             for tup in line:
                 if tup[0] == topic_number and tup[1] >= threshold_topic_weight:
                     print(raw_data[j])



def topic_weights_plot(doc_tops, save_doc=False, save_fig=False):
    import pylab

    top_weight_sum = {}

    for i, line in enumerate(doc_tops):
            num_tops = len(line)
            for tup in line:
                if tup[0] not in top_weight_sum:
                    top_weight_sum[tup[0]] = tup[1]
                if tup[0] in top_weight_sum:
                    top_weight_sum[tup[0]] += tup[1]

    points = []

    for top, weight in top_weight_sum.items():
        points.append((top, weight/len(doc_tops)))

    average_weight = [tup[1] for tup in points][0]/num_tops

    variance = 0
    for top in points:
        variance = variance + (((((len(top) - 1) - average_weight) ** 2) ** 0.5) / average_weight) * 100

    standardabweichung = variance/num_tops

    weights_reverse = [(tup[1], tup[0]) for tup in points]
    weights_sorted = sorted(weights_reverse, reverse=True)



    x, y = list(zip(*points))
    pylab.bar(x, y)
    pylab.title('Topic Weight Sums')
    pylab.ylabel('Sum Weights')
    pylab.xlabel("Topic Nr.")

    # if save_fig:
    #    if engine == 'mallet':
    #        pylab.savefig(user_output + user + '_Mallet_topic_weight_sums_' + name_dataset_mallet + '_' + str(
    #            topics_mallet) + 'topics' + now + '.pdf')
    #    if engine == 'gensim':
    #        pylab.savefig(user_output + user + '_Gensim_topic_weight_sums_' + name_dataset_gensim + '_' + str(
    #            topics_gensim) + 'topics' + now + '.pdf')

    pylab.show()
    return 'Standardabweichung: ' + str(standardabweichung)

    # if save_doc:
    #    if engine == 'mallet':
    #        out = open(user_output + user + '_Mallet_top_weight_sums_' + name_dataset_mallet + '_' + str(
    #            topics_mallet) + 'topics_' + now + '.txt', 'w', encoding='UTF-8')
    #    if engine == 'gensim':
    #        out = open(user_output + user + '_Gensim_top_weight_sums_' + name_dataset_gensim + '_' + str(
    #            topics_gensim) + 'topics_' + now + '.txt', 'w', encoding='UTF-8')
    #    for line in weights_sorted:
    #        out.write(str(line))
    #    out.close()


# def word_count(dataset_wordcount):
#     word_count = 0
#
#     if dataset_wordcount == 'data':
#         dataset_wordcount = data
#     if dataset_wordcount == 'data_words_nostops':
#         dataset_wordcount = data_words_nostops
#     if dataset_wordcount == 'data_final':
#         dataset_wordcount = data_final
#
#     for doc in dataset_wordcount:
#         word_count = word_count + len(doc)
#     return word_count
#

# @markdown Soll nur eine Auswahl von Interviews angezeigt werden? IDs in Textfeld eintragen, kommasepariert.

def doc_top_heatmap(doc_tops, top_words, dataset, split_index=0, save_fig=False, width=1000, height=800):

    import pandas as pd
    import plotly.express as px
    import re
    from datetime import datetime


    #document_search = False  # @param {type:"boolean"}
    #document_id = "ADG0001,ADG0002,ADG0003"  # @param {type:"string"}
    #document_ids_repl = document_id.replace(' ', '')
    #document_ids = [id for id in document_ids_repl.split(',')]

    width = 1000  # @param {type:"integer"}
    height = 800  # @param {type:"integer"}

    now = str(datetime.now())[:19]
    matrix_type = 'doc_top'

    # Keywords für X-Achse

    raw_data = dataset
    output = []
    for line in top_words:
            newline = ''
            for i in range(0, 10):
                newline = newline + str(line[1][i]) + ' '
            output.append([line[0], newline])

    if matrix_type == 'doc_top':

        interview_id = str(raw_data[0][0].split('_')[:split_index])
        interview_topics = {}
        tops_per_int_counter = []
        chunk_count = 1

        for i, line in enumerate(doc_tops):
            if interview_id == str(raw_data[0][0].split('_')[:split_index]):
                for tup in line:
                    if tup[0] not in interview_topics:
                        interview_topics[tup[0]] = tup[1]
                    if tup[0] in interview_topics:
                        interview_topics[tup[0]] += tup[1]
                chunk_count += 1

            try:
                if interview_id != str(raw_data[i][0].split('_')[:split_index]) or i == len(raw_data) - 1:
                    for topic, count in interview_topics.items():
                        tops_per_int_counter.append([interview_id, topic, count / chunk_count])
                    interview_id = str(raw_data[i][0].split('_')[:split_index])
                    interview_topics = {}
                    chunk_count = 1
                    for tup in line:
                        if tup[0] not in interview_topics:
                            interview_topics[tup[0]] = tup[1]
                        if tup[0] in interview_topics:
                            interview_topics[tup[0]] += tup[1]
            except IndexError:
                continue

    #if document_search:
    #    transfer = []
    #    for line in tops_per_int_counter:
    #        if line[0].split('_')[0] in document_ids:
    #            transfer.append(line)
    #    tops_per_int_counter = transfer

    df_heatmap = pd.DataFrame(tops_per_int_counter, columns=['doc', 'top', 'weight'])
    doc_tops_heatmap = df_heatmap.pivot("doc", "top", "weight")
    fig = px.imshow(doc_tops_heatmap, color_continuous_scale='emrld', height=height, width=width, aspect='auto')
    fig.show()