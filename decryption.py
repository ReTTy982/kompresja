from encryption import xor

def decrypt(text,key):
    decrypted = ""
    key_index = 0
    for i in range(len(text)):
        x = format(ord(text[i]),'08b')
        if(key_index == len(key)):
            key_index = 0
        y = format(ord(key[key_index]),'08b')
        decrypted += xor(x,y)
        key_index += 1
    return bytes_to_chr(decrypted)


def bytes_to_chr(text):
    message = ""
    for i in range(0,len(text),8):
        byte = text[i:i+8]
        message += chr(int(byte,2))
    return message

