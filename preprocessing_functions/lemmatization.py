# Noch nicht an die neue Datenstruktur angepasst [14.08.2023]
import spacy
import pickle

def lemmatization(sentence, nlp_model, goldlist, pos_filter: type=bool, allowed_postags=['NOUN', 'PROPN', 'VERB', 'ADJ', 'ADV', 'PRON', 'ADP', 'DET', 'AUX', 'NUM', 'SCONJ', 'CCONJ', 'X']):

    doc = nlp_model(" ".join(sentence))
    if pos_filter:
        sentence_lemmatized = [token.lemma_ for token in doc if token.pos_ in allowed_postags or token.lemma_ in goldlist]
    if not pos_filter:
        sentence_lemmatized = [token.lemma_ for token in doc]

    sentence_lemmatized_out = [word for word in sentence_lemmatized]

    return sentence_lemmatized_out

def lemmatization_test(sentence, nlp_model, goldlist, goldliste_test, pos_filter: type=bool, allowed_postags=['NOUN', 'PROPN', 'VERB', 'ADJ', 'ADV', 'PRON', 'ADP', 'DET', 'AUX', 'NUM', 'SCONJ', 'CCONJ', 'X']):

    doc = nlp_model(" ".join(sentence))

    sentence_lemmatized = [(token.lemma_, token.pos_) for token in doc]

    sentence_lemmatized_filtered = [token.lemma_ for token in doc if token.pos_ in allowed_postags or token.lemma_ in goldlist]

    sentence_lemmatized_out = [word for word in sentence_lemmatized_filtered]


    for word in sentence_lemmatized:
        if word[0] not in sentence_lemmatized_filtered:
            goldliste_test.append(word)


    # hier txt-Datei aus Liste erstellen


    return sentence_lemmatized_out, goldliste_test

###############
### TESTING ###
###############

# spacy_model = spacy.load('de_core_news_lg', disable=['parser', 'ner'])
# goldlist = ['bayrisch']
#
#
# x=lemmatization_test(['ich', 'kriege', 'die', 'Krise', 'Diese', 'Kriege', 'sind', 'schrecklich', 'Kriege', 'ich', 'noch', 'etwas', 'bayrisch'], spacy_model, goldlist, pos_filter=True, allowed_postags=['NOUN', 'PROPN', 'VERB', 'ADJ', 'NUM'])
# print(x)