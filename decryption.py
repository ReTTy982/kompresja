from encryption import xor

def decrypt(text,key):
    decrypted = ""

    for i in range(len(text)):
        x = format(ord(text[i]),'08b')
        y = format(ord(key[i]),'08b')
        decrypted += xor(x,y)
    return decrypted

