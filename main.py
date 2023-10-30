from decompress import *
from comperss import *
from encryption import encrypt,generate_key
from decryption import decrypt

message = "asjcinqowinmoqidjq781sjasjajksASKJDH"
compressed_message = start_compress(message)
decompressed_message = decompress_text(compressed_message)
key = generate_key(len(compressed_message))
encrypted_message = encrypt(compressed_message,key)
decrypted_message = decrypt(encrypted_message,key)



print('\n')
print(f"WIADOMOSC: {message}\n")
print(f"Skompresowana wiadomsoc: {compressed_message}\n")
print(f"Dekompresowana wiadomosc: {decompressed_message}")
print(f"Klucz: {key}")
print(f"")