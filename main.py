from decompress import *
from comperss import *
from encryption import encrypt,generate_key
from decryption import decrypt
message = "ABAJNCKJASNDUJHQWIUDHSJKHDUIQWHDJASHDASDKJANCZXM<CNHIUQWHJABAJNCKJASNDUJHQWIUDHSJKHDUIQWHDJASHDASDKJANCZXM<CNHIUQWHJABAJNCKJASNDUJHQWIUDHSJKHDUIQWHDJASHDASDKJANCZXM<CNHIUQWHJABAJNCKJASNDUJHQWIUDHSJKHDUIQWHDJASHDASDKJANCZXM<CNHIUQWHJ"
with open("_uncoded.txt", "w",encoding="utf-8") as file:
    text = message
    file.write(text)
with open("_uncoded.txt", "r",encoding="utf-8") as file:
    read_text = file.read()
    
compressed_message = start_compress(read_text)

with open("_coded.txt", "w",encoding="utf-8") as file:
    file.write(compressed_message)

    
decompressed_message = decompress_text(compressed_message)  
key = generate_key(32)
encrypted_message = encrypt(compressed_message,key)
decrypted_message = decrypt(encrypted_message,key)
decrypted_decompressed_message = decompress_text(decrypted_message)




print('\n')
print(f"WIADOMOSC: \n{message}\n")
print(f"Skompresowana wiadomsoc: \n{compressed_message}\n")
print(f"Dekompresowana wiadomosc: \n{decompressed_message}\n")
print(f"Klucz: {key}")
print(f"Zakodowana wiadomość: {encrypted_message}")
print(f"Odkodowana wiadomość {decrypted_message}")
print(f"Dekompresowana wiadomość po odkodowaniu: {decrypted_decompressed_message}") 