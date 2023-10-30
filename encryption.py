import random
def generate_key(size):
    key = ""
    for i in range(size):
        key +=chr(random.randrange(33,127))
    return key

def encrypt(text,key):
    encrypted = ""

    for i in range(len(text)):
        x = format(ord(text[i]),'08b')
        y = format(ord(key[i]),'08b')
        encrypted += xor(x,y)
    return bytes_to_chr(encrypted)


def print_xor(x,y,z):
    print(x)
    print(y)
    print(z)
    print("--------------")


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

message = "asdijasiodj"
key=generate_key(len(message))
coded_message= encrypt(message,key)
