def decrypt_text(text):
    alphabet_length  = ord(text[0])
    alphabet = text[1:alphabet_length+1]
    for character in text:
        byte = format(ord(character),'008b')
        for pair in byte:
            print(pair)