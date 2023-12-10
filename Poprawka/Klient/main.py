import requests
from Crypto.PublicKey import RSA
import json
import base64
from Crypto.Cipher import PKCS1_v1_5




class RequestManager:
    url = "http://localhost:5000/"
    
    @staticmethod
    def register(username, password, public_key):
        response = requests.post(url=RequestManager.url+'register',
                                json={
                                    'username': username,
                                    'password': password,
                                    'public_key': public_key.decode('utf-8')
                                },
                                headers={'Content-Type': 'application/json'})
        return response
        
    @staticmethod
    def login(username,password,public_key):
        response = requests.post(url=RequestManager.url+'login',
                                json={
                                    'username': username,
                                    'password': password,
                                    'public_key': public_key.decode('utf-8')
                                },
                                headers={'Content-Type': 'application/json'}
                                )
        return response
    
    @staticmethod
    def send_message(token,receiver,message):
        response = requests.post(url=RequestManager.url+'message',
                                 json={'receiver':receiver,
                                       'text':message},
                                 headers={
                                    'Content-Type': 'application/json',
                                    'Authorization': token 
                                 })
        return response
        
    @staticmethod
    def get_messages(token):
        response = requests.get(url=RequestManager.url,
                                headers={
                                    'Authorization': token 
                                 })
        return response
    
    


class LocalManager:
    @staticmethod
    def generate_rsa_key():
        key =RSA.generate(2048)
        return key.public_key().export_key()
    
    @staticmethod
    def encode_message(message,public_key):
        p = RSA.import_key(public_key)
        cipher = PKCS1_v1_5.new(p)
        encrypted_text = cipher.encrypt(message.encode('utf8'))
        encoded_message = base64.b64encode(encrypted_text).decode('utf-8')
        return encoded_message
    
    @staticmethod
    def decode_message(message,public_key):
        key = RSA.import_key(public_key)
        cipher = PKCS1_v1_5.new(key)
        print(message)
        decrypted_message = cipher.decrypt(base64.b64decode(message), None)
        #print(decrypted_message)

        
    
    
    
class AppManager:
    session_token = None
    session_key = None
    
    def run(self):
        #self.register_user("3","1")
        self.login_user("3","1")
        self.send_message("1","Hello world2!")
        self.get_messages()
        
    
    def login_user(self,username,password):
        public_key = LocalManager.generate_rsa_key()
        response = RequestManager.login(username,password,public_key)
        data = response.json()
        server_public_key = data['public_key']
        token = data['token']
        AppManager.session_token = token
        AppManager.session_key = server_public_key
    
    def register_user(self,username,password):
        public_key = LocalManager.generate_rsa_key()
        response = RequestManager.register(username,password,public_key)
        data = response.json()
        server_public_key = data['public_key']
        token = data['token']
        
    def send_message(self,receiver,message):
        message = LocalManager.encode_message(message,AppManager.session_key)
        response = RequestManager.send_message(self.session_token,receiver,message)
        if response.status_code == 400:
            print(response.text)
    
    def get_messages(self):
        response = RequestManager.get_messages(self.session_token)
        data = response.json()
        LocalManager.decode_message(data[0]['text'],self.session_key)
   
if __name__ == "__main__":
    app = AppManager()
    app.run()