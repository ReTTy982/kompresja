



def get_alphabet(file_string):
	dictionary = []
	for symbol in file_string:
		if symbol not in dictionary:
			dictionary.append(symbol)
	return dictionary
 


def encode_fixed_length(text,alphabet,):
	
	code_length = (len(alphabet)-1).bit_length()
	encoded_text = ''
	for char in text:
		char_index = alphabet.index(char)
		char_code = format(char_index, '0' + str(code_length) + 'b')
		encoded_text += char_code

	
	return encoded_text

def change_to_bits(message):
	
	coded_message = ""
	
	
	first_bits = format(0,'03b')
	message = first_bits + message
	text_length = len(message)
	additional_bits = 8 - (text_length % 8)

	if additional_bits > 0:
		message = format(additional_bits,'03b') + message[3:]
	
	for i in range(0, text_length, 8):
		chunk = message[i:i + 8]
		if len(chunk) < 8:
			for i in range(additional_bits):
				chunk = chunk + "1"
			
			coded_message += chr(int(chunk,2))
		else:
			coded_message += chr(int(chunk,2))
	return coded_message


def start_compress(file_string):
	
	alphabet = get_alphabet(file_string)
	encoded_message = encode_fixed_length(file_string, alphabet)
	return_value = chr(len(alphabet)) +  "".join(alphabet) + change_to_bits(encoded_message)
	print(return_value)
	return return_value
 

 
 
 
	