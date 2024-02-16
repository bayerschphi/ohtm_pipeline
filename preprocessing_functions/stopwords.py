def remove_speaker(data):

    '''Removes Speaker from flat lists of Words - Case Sensitive!'''

    for i, word in enumerate(data):
        if "INT_" in word:
            if not word.startswith("INT_"):         # in sehr seltenen Fällen könnte es sein, dass ein Wort am
                word_clean = word.split('INT_')[0]  # Sprecherwechsel klebt - dann kann man nicht splitten, weil man das
                data.pop(i)                         # komplette Kürzel nicht kennt und die Kürzel auch unterschiedlich
                data.insert(i, word_clean)          # lang sein können (wir haben INT_A und INT_AvP z.B.)
                                                    # daher würde ich "INT_APgegangen" usw. einfach rausschmeißen
                                                    # wenn der Sprecherwechsel an einem Wort klebt, ist es kein Problem
                                                    # gegangenINT_AP -> Split an "INT_", Splitliste an Stelle 0 behalten
            else:
                data.pop(i)

        if "IP_" in word:
            if not word.startswith("IP_"):
                word_clean = word.split('INT_')[0]
                data.pop(i)
                data.insert(i, word_clean)
            else:
                data.pop(i)


    return data

def remove_stopwords_by_list(data, stoplist):
    data_out = [word for word in data if word.lower() not in stoplist]
    return data_out


def remove_particles(data):       # Partikel
    data_out = []
    for word in data:
        word_set = set(word)
        if len(word_set) == 3:
            if "ä" and "h" and "m" in word_set:
                if word[0] == "ä":
                    next
                else:
                    data_out.append(word) # Diese Ausnahme ist nur für das wort "mäh" gedacht.
            else:
                data_out.append(word)
        elif len(word_set) == 2:
            if "h" in word_set:      # Check if "hm" and "äh" and "ah" in different forms are in the text. They are removed. all Words < 2 are removed.
                if "m" in word_set:
                    next
                elif "ä" in word_set:
                    next
                elif "a" in word_set:
                    next
                else:
                    data_out.append(word)
            if "sa" in word:        # SA is not removed
                data_out.append(word)
            else:
                data_out.append(word)
        elif len(word_set) == 1:
            if "ss" in word:        # SS is not removed
                data_out.append(word)
            else:
                next
        elif len(word_set) == 0:
            next

        else:
            data_out.append(word)
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
