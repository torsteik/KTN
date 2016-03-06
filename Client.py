# -*- coding: utf-8 -*-
import socket
import MessageReceiver
import json


class Client:
    """
    This is the chat client class
    """
    
    ## MIN KODE
    #server_port
    ## SLUTT
    
    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """

        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # TODO: Finish init process with necessary code
        ## MIN KODE
        self.host = host
        self.server_port = server_port
        
        self.Receiver = MessageReceiver.MessageReceiver(self, self.connection) #SENDER PARSEREN TIL ASTRIT
        self.isLoggedin = False
        ## SLUTT
        print "init complete... Connecting"
        self.run()

    def run(self):
        # Initiate the connection to the server
        notConn = True
        while notConn:
            try:
                self.connection.connect((self.host, self.server_port))
            except:
                ans = raw_input("Can't connect, try again? (y/n)")
                if ans == "y":
                    continue
                elif ans == "n":
                    exit()
                else:
                    print "Invalid answer"
                    continue
            notConn = False
        print "Connection established\nType -help for help"
        print "Type -login [username] to log in"
        self.Receiver.start()
    
        while True:
            msg = raw_input()
            if len(msg) > 0:
                payload = self.interpret_req(msg)
                if payload == -1:
                    continue
                try:
                    payload = json.dumps(payload)
                except:
                    print "ERROR: BAD MESSAGE (can't use æ, ø or å)"
                    continue
                self.send_payload(payload)
                if ('"request": "logout"' in payload):
                    self.disconnect()                        
        
    
    def disconnect(self):
        print "Shutting down"
        self.connection.close()
        raw_input("Press any button to close program\n")
        exit()

    def send_payload(self, data):
        totalsent = 0
        MSGLEN = len(data)
        while totalsent < MSGLEN:
            sent = self.connection.send(data[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent += sent
            
        
    # More methods may be needed!

    def interpret_req(self, msg):
        if msg[0] == "-":
            if "-login" in msg:
                if len(msg.split()) != 2:
                    print "ERROR: INVALID LOGIN"
                    return -1
                else:
                    if not self.isLoggedin:
                        self.username = msg.split()[1]
                    return {'request':'login', 'content':msg.split()[1]}
                
            elif "-names" in msg:
                return {'request':'names', 'content':""}
            
            elif "-help" in msg:
                return {'request':'help', 'content':""}
            
            elif "-logout" in msg:
                return {'request':'logout', 'content':""}
        
        return {'request':"msg", 'content':msg}


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
#129.241.206.176
    
