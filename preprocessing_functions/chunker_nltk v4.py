def chunker_nltk(input_file, max_words=50, output_file='C:\\Users\\moebusd\\Desktop\\Chunker\\output\\'):
    from odf.opendocument import load as load_odf
    from odf import text as odf_text, teletype
    from odf.opendocument import OpenDocumentText
    from odf.text import P
    import re
    import nltk
    nltk.download('punkt')
    # Name der Ausgabedatei
    if output_file == '':
        output_file = input_file.replace('.odt', '_new.odt')
    else:
        output_file = output_file + input_file.split('\\')[-1].replace('.odt', '_new.odt')
    report_file = input_file.replace('.odt', '_sprecher.txt')
    report_file2 = input_file.replace('.odt', '_ueberschrift.txt')
    observations = ''
    headlines = ''
    list_sentences = []
    # Sprechende Person, steht immer am Zeilenanfang. Nur Großbuchstaben o. Bodenstrich
    # fehlt die Angabe am Zeilenanfang, wird der Text der letzten erkannten Person zugeordnet
    pattern1 = r'([A-Z]+_[A-Z]+)([ :]*)\[?'
    # Interpunktions- und Sonderzeichen, die (alleinstehend) nicht als Wörter gezählt werden sollen
    pattern2 = r'[\!\"\'\`\*\+\,\.\/\:\;\?\\\{\|\}\(\) ]+'
    # Ein Fragezeichen, das vor einer Klammer steht, wandert in die Klammer
    # Ich fuhr nach ? (Hagen) zur Uni → Ich fuhr nach (Hagen?) zur Uni
    pattern3 = r'(\? ?)(\(.*?)\)'
    # öffnende Klammer, die im Satz nicht mehr geschlossen wird
    pattern4 = r'\(((?!\)).)*$'
    # schließende Klammer ohne vorherige öffnende im Satz
    pattern5 = r'^((?!\().)*\)'
    # Sprecher in Zeile
    pattern6 = r'[A-Z]+_[A-Z]+'
    # öffnende eckige Klammer, die im Satz nicht mehr geschlossen wird
    pattern7 = r'\[((?!\]).)*$'
    # schließende eckige Klammer ohne vorherige öffnende im Satz
    pattern8 = r'^((?!\[).)*\]'
    # Korrekturen Interpunktion
    repl_list1 = [('. ..', '...'),
                  ('.. .', '...'),
                  ('. .', '..'),
                  ('?.', '?'),
                  ('? .', '?'),
                  ('?..', '?'),
                  ('? ?', '???'),
                  ('! !', '!!!'),
                  ('** ?', '???'),
                  ('**?', '???'),
                  ('* ?', '???'),
                  ('* *?', '???'),
                  ('? )', '?)'),
                  ('! )', '!)'),
                  ('. )', '.)'),
                  ('.".', '."')]
    # Falls Datei ohne Sprecherangabe beginnt, Defaultwert XXX
    z = 'XXX'
    odf_file = load_odf(input_file)
    # auf Formatierungen im odt prüfen. Überschriften separat speichern
    all_headers = odf_file.getElementsByType(odf_text.H)
    if all_headers:
        for para in all_headers:
            line = teletype.extractText(para).strip()
            if len(line) == 0:
                continue
            else:
                headlines = headlines + "Als Überschrift formatiert:\n" + line + "\n\n"
    all_paras = odf_file.getElementsByType(odf_text.P)
    # Zeilen aus odt extrahieren
    # weiche Zeilenumbrüche durch harte ersetzen, leere Zeilen löschen
    new_para_list = []
    for para in all_paras:
        line = teletype.extractText(para).strip()
        if len(line) == 0:
            continue
        soft_break = chr(10)
        list_s = line.split(soft_break)
        new_para_list.extend(list_s)
    # Liste mit Zeilen abarbeiten
    for line in new_para_list:
        # Interpunktion korrigieren
        for r1 in repl_list1:
            line = line.replace(r1[0], r1[1])
        # Fragezeichen in die Klammern verschieben
        line = re.sub(pattern3, '\\2?)', line)
        # Sprecher erkennen und aus der Zeile entfernen
        match_first = re.match(pattern1, line)
        if match_first:
            z = match_first.group(1)
            sum_len = len(match_first.group(1)) + len(match_first.group(2))
            line = line[sum_len:]
        # Wenn Sprecher mitten in der Zeile, dann entfernen
        match_in_line = re.search(pattern6, line)
        if match_in_line:
            observations = observations + "Sprecherkürzel mitten in der Zeile:\n" + line + "\n\n"
        # Weicher Umbruch
        if chr(10) in line:
            observations = observations + "Weicher Zeilenumbruch:\n" + line + "\n\n"
        # Sätze identifizieren
        sentences = nltk.sent_tokenize(line, language='german')
        for y in sentences:
            # Wörter identifizieren
            words = nltk.word_tokenize(y, 'german')
            # Satz- und Sonderzeichen nicht als Wörter zählen
            filtered_words = [token for token in words if not (re.search(pattern2, token))]
            # Sprecher, Zahl der Wörter, Satz in Liste m. Zähler schreiben
            wordcount = len(filtered_words)
            list_sentences.append((z, wordcount, y))
    # Liste der Elemente der neu zusammengebauten Sätze
    nl = [0]
    # Gesamtliste aller neuen Sätze. Kann zur Kontrolle verwendet werden, dient nicht für den Output
    newlist = []
    # gesamter neuer Text. Funktion wie nl
    whole_text = ''
    # Vor der Schleife erste Zeile einlesen, damit dort Vergleich funktioniert
    speaker, wordc, ntextsp = list_sentences[0]
    all_w = wordc
    wl = speaker + ': ' + ntextsp
    for x in range(len(list_sentences)-1):
        # öffnende Klammer ohne folgende schließende im vorhergehenden Satz
        missing_opening_br_before = re.search(pattern4, ntextsp)
        # Falls keine runde Klammer, auf eckige prüfen
        if not(missing_opening_br_before):
            missing_opening_br_before = re.search(pattern7, ntextsp)
        nspeaker, nwordc, ntextsp = list_sentences[x + 1]
        # schließende Klammer ohne vorherige öffnende im aktuellen neuen Satz
        missing_closing_br = re.search(pattern5, ntextsp)
        # Falls keine runde Klammer, auf eckige prüfen
        if not(missing_closing_br):
            missing_closing_br = re.search(pattern8, ntextsp)
        # → satzübergreifende Klammerstruktur
        bracket_str = missing_closing_br and missing_opening_br_before
        # gleicher Sprecher und weniger als max_words Wörter oder aber satzübergreifende Klammer
        if speaker == nspeaker and ((all_w + nwordc <= max_words) or bracket_str):
            # Folgesatz an wl anhängen
            nl.append(x + 1)
            wl = wl + ' ' + ntextsp
            all_w = all_w + nwordc
        # Sprecherwechsel oder über max_words Wörter, keine satzübergreifende Klammer
        else:
            # Vorsatz und Zeilenumbruch an whole_text anhängen, Folgesatz mit Sprecher neu beginnen
            newlist.append(nl)
            whole_text = whole_text + wl + '\n'
            speaker = nspeaker
            all_w = nwordc
            nl = [x + 1]
            wl = nspeaker + ': ' + ntextsp
    # letzten Satz am Ende der Schleife verarbeiten (x+1)
    newlist.append(nl)
    whole_text = whole_text + wl
    # Wegschreiben
    doc_out = OpenDocumentText()
    for line in whole_text.splitlines():
        doc_out.text.addElement(P(text=line))
        doc_out.text.addElement(P(text=''))
        doc_out.save(output_file)
    # Sprecher in Zeile speichern
    if len(observations) > 0:
        with open(report_file, 'w') as file:
            file.write(observations)
    # Headline-Formatierung speichern
    if len(headlines) > 0:
        with open(report_file2, 'w') as file:
            file.write(headlines)


# Aufruf der Funktion mit Testdatei
# Syntax chunker_nltk(Eingabedatei m. Pfad, Maximum Wörter pro Zeile, Ausgabedatei m. Pfad)
import os
for file in os.listdir('C:\\Users\\moebusd\\Desktop\\Chunker'):
    if file.lower().startswith('adg') and file.endswith('odt'):
        chunker_nltk('C:\\Users\\moebusd\\Desktop\\Chunker\\' + file)
        print(file)