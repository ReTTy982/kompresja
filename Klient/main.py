import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import json


class ServerConnection:
    def __init__(self,url,token=None):
        self.url = url
        self.token = token
        
        
    def register(self,username,password,public_key):
        try:
            response = requests.post(url=self.url+"/register",
                                     json={"username" : username, "password" : password, "public_key" : public_key})
            response.raise_for_status()
            if response.status_code == 201:
                self.token = response.json()['token']
                print(response.json()['public_key'])
                return response.json()
            
        except requests.exceptions.RequestException as e:
            print(e)
            
            
    def login(self,username,password,public_key):
        try:
            response = requests.post(url=self.url+"/login",
                                     json={"username" : username, "password" : password, "public_key": public_key,})
            response.raise_for_status()
            if response.status_code == 200:
                self.token = response.json()["token"]
        except requests.exceptions.RequestException as e:
            print(e)
            
            
    def send_message(self,receiver,message):
        try:
            response = requests.post(self.url+"/message",
                                     json={"receiver" : receiver, "text" : message},
                                     headers={"Authorization" : self.token})
            response.raise_for_status()
            print(response.status_code)
            print(response.content)
        except requests.exceptions.RequestException as e:
            print(f"Send Message Error: {e}")
   
   
    def get_message(self,private_key):
        try:
            response = requests.get(self.url + "/",headers={"Authorization" : self.token})
            response.raise_for_status()
            for body in response.json():
                coded_message = body["text"]
                decoded_message = MessageCoder.decode_rsa(coded_message,private_key)
                print(decoded_message)

        except requests.exceptions.RequestException as e:
            print(e)
   
class User:
    def __init__(self,username,private_key=None,public_key=None,server_public_key=None):
        self.username = username
        self.private_key = private_key
        self.public_key = public_key
        self.server_public_key = server_public_key
        self.public_key_str = None
  
    

class Sesion:
    def __init__(self,user : User,server_connection : ServerConnection, token=None):
        self.user = user
        self.server_connection = server_connection
        self.token = token
        
    def send_message(self,reciver,message):
        message_encoded = MessageCoder.code_rsa(message,self.user.public_key)
        self.server_connection.send_message(reciver,message_encoded)
    def login(self,password):
        #self.get_user()
        self.server_connection.login(self.user.username,password,self.user.public_key_str)
        if self.server_connection.token != None:
            print("Udalo sie")
    def register(self,password):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
          
        pem_public_key = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        public_key_str = pem_public_key.decode('utf-8')
        self.public_key_str = public_key_str
  

        private_key_str = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')
        json_data = self.server_connection.register(self.user.username,password,public_key_str)
        if json_data is not None:
            self.token = json_data['token']
            self.user.server_public_key = json_data['public_key']
            self.user.public_key  =public_key
            self.user.private_key = private_key
            # self.save_user()
    
    def save_user(self):
        try:
            with open("user.json",'r') as read_file:
                json_data_read = json.load(read_file)
                json_data_read[self.user.username] = {'private_key' : self.user.private_key , 'public_key' : self.user.public_key, 'server_public_key' : self.user.server_public_key}
        except FileNotFoundError:
            json_data_read = {}
            json_data_read[self.user.username] = {'private_key' : self.user.private_key , 'public_key' : self.user.public_key, 'server_public_key' : self.user.server_public_key}

        with open ("user.json",'w') as file:
            json.dump(json_data_read,file)
   
    def get_user(self):
       with open("user.json",'r') as read_file:
            json_data_read = json.load(read_file)
            data = json_data_read[self.user.username]
            self.user.private_key = data['private_key']
            self.user.server_public_key = data['server_public_key']
            self.user.public_key = data['server_public_key']
    
    def get_messages(self):
        self.server_connection.get_message(self.user.private_key)
                
            
        
        
        
   
class MessageCoder:
    
    @staticmethod
    def serialize_public_key(public_key):
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode("utf-8")

    @staticmethod
    def deserialize_public_key(serialized_key):
        return serialization.load_pem_x509_certificate(
            serialized_key.encode("utf-8"),
            backend=default_backend()
        ).public_key()
    
    @staticmethod
    def code_rsa(message, public_key):
        ciphertext = public_key.encrypt(
            message.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        encoded_message = base64.b64encode(ciphertext).decode("utf-8")
        return encoded_message
    
    
    @staticmethod
    def decode_rsa(encoded_message, private_key):
        ciphertext = base64.b64decode(encoded_message)
        
        decoded_message = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decoded_message.decode("utf-8")
    
    @staticmethod
    def key_to_string(key):
        if isinstance(key, rsa.RSAPublicKey):
            return MessageCoder.serialize_public_key(key)
        elif isinstance(key, rsa.RSAPrivateKey):
            return key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode("utf-8")
        else:
            raise ValueError("Unsupported key type")

    @staticmethod
    def string_to_key(key_str, key_type):
        if key_type == "public":
            return MessageCoder.deserialize_public_key(key_str)
        elif key_type == "private":
            return serialization.load_pem_private_key(
                key_str.encode("utf-8"),
                password=None,
                backend=default_backend()
            )
        else:
            raise ValueError("Unsupported key type")
            
if __name__ == "__main__":
    connection = ServerConnection("http://127.0.0.1:5000")
    user = User("Paul123")
    sesion = Sesion(user,connection)
    sesion.register("123")
    sesion.login("123")
    sesion.send_message("aaaaaaaaaasdsaaaa","Hello")
    sesion.get_messages()
    
    
 
 
 
 

    # msg = "Jakas wiadomsoc"
    
    # encoded_message = MessageCoder.code_rsa(msg,public_key)
 
    
    

    
    

    #session.register("retttty","123",public_key_str)
    # session.login("retttty","123",public_key_str)
    # session.send_message("retty",encoded_message)
    # session.get_message()
