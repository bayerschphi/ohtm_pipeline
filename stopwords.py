def remove_stopwords_by_list(data, stoplist):
    data_out = [[word for word in line if word not in stoplist] for line in data]
    return data_out


def remove_stopwords_by_threshold(data, threshold):
    wordcounts = {}
    wordcount = 0

    for line in data:
        wordcount = wordcount + len(line)

    for line in data:
        for word in line:
            if word in wordcounts:
                wordcounts[word] += 1
            if word not in wordcounts:
                wordcounts[word] = 1

    wordcounts_sorted = []

    for word, count in wordcounts.items():
        t = ((count / wordcount) * 100, count, word)
        wordcounts_sorted.append(t)

    wordcounts_out = sorted(wordcounts_sorted, reverse=True)

    stoplist_by_threshold = [word[2] for word in wordcounts_out if word[0] > threshold]

    data_out = [[word for word in line if word not in stoplist_by_threshold] for line in data]
    return data_out
