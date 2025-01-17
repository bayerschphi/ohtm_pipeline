"""
Removes Speaker from flat lists of Words - Case Sensitive!
"""


def remove_speaker(data):
    for i, word in enumerate(data):
        if "INT_" in word:
            word_clean = word.replace('INT_', '')
            data.pop(i)
            data.insert(i, word_clean.lower())

        if "IP_" in word:
            word_clean = word.replace('IP_', '')
            data.pop(i)
            data.insert(i, word_clean.lower())

    return data


def remove_stopwords_by_list(data, stoplist):
    data_out = [word for word in data if word.lower() not in stoplist]
    return data_out


def remove_particles(data):
    print("Not included so far")
    # To be done


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
