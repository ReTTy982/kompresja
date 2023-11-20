import random
def generate_key(size):
    key = ""
    for i in range(size):
        key +=chr(random.randrange(33,127))
    return key

def encrypt(text,key):
    encrypted = ""
    key_index = 0
    for i in range(len(text)):
        x = format(ord(text[i]),'08b')
        if (key_index == len(key)):
            key_index = 0
        y = format(ord(key[key_index]),'08b')
        encrypted += xor(x,y)
        key_index += 1
    return bytes_to_chr(encrypted)

def xor(x,y):
    encrypted_byte = ""
    for i in range(8):
        if x[i] == y[i]:
            encrypted_byte += "0"
        else:
            encrypted_byte += "1"
        
    return encrypted_byte

def bytes_to_chr(text):
    message = ""
    for i in range(0,len(text),8):
        byte = text[i:i+8]
        message += chr(int(byte,2))
    return message


