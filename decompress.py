def decompress_text(text):
    alphabet_length  = ord(text[0])
    alphabet = list(text[1:alphabet_length+1])
    
    binary_string = create_binary(text[alphabet_length+1:])
    bit_for_sign = (alphabet_length-1).bit_length()
    final_string = ""

    for character in text:
        byte = format(ord(character),'008b')
        #for pair in byte:
    
    for i in range(0,len(binary_string),bit_for_sign):
        chunk = binary_string[i:i+bit_for_sign]
        index = int(chunk,2)
        final_string = final_string + alphabet[index]
    return final_string


def create_binary(text):
    output_string=""
    for character in text:
        output_string = output_string + format(ord(character),'08b')
    filler = int(output_string[0:3],2)
    output_string = output_string[3:]
    output_string = output_string[:-filler]
    return output_string

def match_dictionary(bits,alphabet):
    return 