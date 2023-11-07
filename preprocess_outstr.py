def preprocess_outstr(text):
    
    text = text.lower() ## Majuskeln durch Minuskeln ersetzen
    
    text = text.replace('\n', ' ').replace('- ', '') ## Zeilenumbrüche entfernen

    text_alpha = text

    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'Ä', 'Ö', 'Ü', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'ä', 'ö', 'ü', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'ß', ' ', '*']
    punct_a = []
    punct_b = ['/'] ## Liste mit Schrägstrich

    for i in text_alpha:
            if i not in alphabet:
                if i not in punct_a:
                    if i != '/' or '\t':
                        punct_a.append(i)
                if i in punct_a:
                    continue    
    
    text_norm = text ## Interpunktion entfernen

    for char in text_norm:
        if char in punct_a:
            text_norm = text_norm.replace(char, '')
        if char in punct_b:
            text_norm = text_norm.replace(char, ' ')
            
    text_clean = text_norm
    
    while '  ' in text_clean:
        text_clean = text_clean.replace('  ', ' ') ## überschüssige Leerzeichen entfernen

    return text_clean

#from plain_transcript import plain_transcript
#text = plain_transcript('Alexander', 'Johanna')
#tokens = preprocess_lusir_query('text')
#print(tokens)
#print(text)