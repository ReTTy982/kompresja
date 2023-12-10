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
        return key
        return key.public_key().export_key()
    
    @staticmethod
    def encode_message(message,public_key):
        p = RSA.import_key(public_key)
        cipher = PKCS1_v1_5.new(p)
        encrypted_text = cipher.encrypt(message.encode('utf8'))
        encoded_message = base64.b64encode(encrypted_text).decode('utf-8')
        return encoded_message
    
    @staticmethod
    def decode_message(message,private_key):
        key = RSA.import_key(private_key)
        cipher = PKCS1_v1_5.new(key)
        decrypted_message = cipher.decrypt(base64.b64decode(message), None)
        return decrypted_message

        
    
    
    
class AppManager:
    session_token = None
    public_key = None
    private_key = None
    server_public_key = None
    contact_book = {}
    username = None
       
    def run(self):
        user_input = input("Choose option")
        match user_input:
            case '1':
                username = input("Username: ")
                password = input("Password: ")
                self.register_user(username,password)
            case '2':
                username = input("Username: ")
                password = input("Password: ")
                self.login_user(username,password)
            case _:
                self.run()
        data = self.get_messages()
        len_messages = self.init_message_history(data) 
        
        receiver = input("Open conversation with: ")
        self.show_message_history(receiver)
        
        while True:
            user_input = input()
            self.send_message(receiver,user_input)
            data = self.get_messages()
            self.init_message_history(data)
            self.show_message_history(receiver) 
        
            
        #self.register_user("c","1")
        self.login_user("b","1")
        self.send_message("c","ELO!")
        data = self.get_messages()
        self.init_message_history(data)
        self.show_message_history('c')
        
        

        
        
        
    def login_user(self,username,password):
        # Generate keys
        key = LocalManager.generate_rsa_key()
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        AppManager.private_key = private_key
        AppManager.public_key = public_key
        
        # Send request
        response = RequestManager.login(username,password,AppManager.public_key)
        data = response.json()
        server_public_key = data['public_key']
        token = data['token']
        
        AppManager.session_token = token
        AppManager.server_public_key = server_public_key
        AppManager.username = username


    
    def register_user(self,username,password):
        # Generate keys
        key = LocalManager.generate_rsa_key()
        private_key = key.export_key()
        public_key = key.publickey().export_key()
        
        AppManager.private_key = private_key
        AppManager.public_key = public_key
        
        # Send request
        response = RequestManager.register(username,password,public_key)
        data = response.json()
        server_public_key = data['public_key']
        token = data['token']
        
        AppManager.server_public_key = server_public_key
        AppManager.session_token = token
        AppManager.username = username

        
    def send_message(self,receiver,message):
        message = LocalManager.encode_message(message,AppManager.server_public_key)
        response = RequestManager.send_message(self.session_token,receiver,message)
        if response.status_code == 400:
            print(response.text)
    
    def get_messages(self):
        response = RequestManager.get_messages(self.session_token)
        data = response.json()
        return data
        
    def init_message_history(self,data):
        for record in data:
            contact = None
            reciever = record['receiver']
            sender = record['sender']
            if reciever != AppManager.username:
                self.check_contact_book(reciever)
                contact = reciever
            else:
                self.check_contact_book(sender)
                contact = sender
            AppManager.contact_book[contact].append(record)
        return len(AppManager.contact_book[contact])
            
            
    def check_contact_book(self,contact):
        if contact not in AppManager.contact_book.keys():
            AppManager.contact_book[contact] = []
            
            
    def show_message_history(self,contact):
        history = AppManager.contact_book[contact]
        for data in history:
            message = LocalManager.decode_message(data['text'],AppManager.private_key)
            datetime = data['datetime']
            sender = data['sender']
            print(f"[{datetime}] {sender} : {message.decode('utf-8')}")
        
if __name__ == "__main__":
    app = AppManager()
    app.run()