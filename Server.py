# -*- coding: utf-8 -*-
import SocketServer
import datetime
import select
import json
import time

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
users = []
msg_log = []

def username_validation(username):
    valid = 1 # Valid username
    # Check if characters are legal
    for i in range(len(username)):
        int_val = ord(username[i])
        if  (int_val > 47 and int_val < 58) or \
            int_val > 64 and int_val < 91 or \
            int_val > 96 and int_val < 122:
            pass
        else:
            valid = 2 # Invalid username
            break
    # Check if username is free
    if valid == 1 and username in users:
        valid = 3 #Username already in use
    return valid

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """
    
    def handle(self):
        print "Client connected"
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        time_format = "%a %b %d %H:%M:%S %Y"
        username = None
        log_len = len(msg_log)
        message = {
            'timestamp':'',
            'sender':'',
            'response':'',
            'content':''
        }

        # Loop that listens for messages from the client
        while True:
            read, write,exep = select.select([self.connection],[],[],0.2)
            if len(read):
                # If anything was received
                received_string = self.connection.recv(4096)
                received_dict = json.loads(received_string)
                request = received_dict['request']
                content = received_dict['content']
                print "request: ", request, "\ncontent: ", content, "\n"

                # Set timestamp
                message['timestamp'] = datetime.datetime.today().strftime(time_format)

                # Handle received_string
                # sjekk om du kan faktorisere ut .send(message)
                if username:
                    if request == 'login':
                        # User is already logged in
                        message['sender'] = 'Server'
                        message['response'] = 'error'
                        message['content'] = 'Error. Already logged in.'
                        self.connection.send(json.dumps(message))
                        
                    elif request == 'logout':
                        # Logout requested
                        users.remove(username)
                        message['sender'] = 'Server'
                        message['response'] = 'message'
                        message['content'] = username + ' has logged out'
                        msg_log.append(message)
                        self.connection.close()
                        break 

                    elif request == 'msg':
                        # Client requests message broadcast
                        message['sender'] = username
                        message['response'] = 'message'
                        message['content'] = content
                        msg_log.append(json.dumps(message))
                        ######## OBS! INGEN .SEND() OG FAKTORISERE UT HER
                            
                    elif request == 'names':
                        # Client requests list of users in chat
                        message['sender'] = 'Server'
                        message['response'] = 'info'
                        message['content'] = 'Users in chat:'
                        for user in users:
                            message['content'] += '\n' + user
                        self.connection.send(json.dumps(message))
                        
                    elif request == 'help':
                        # Help requested
                        message['sender'] = 'Server'
                        message['response'] = 'info'
                        message['content'] = ('The servers available requests are:\n'
                                                'login<username>    -log in with the given username\n'
                                                'logout             -log out\n'
                                                'msg<message>       -send message\n'
                                                'names              -list users in chat\n'
                                                'help               -view help text')
                        self.connection.send(json.dumps(message))
                        
                    else:
                        #ERROR
                        message['sender'] = 'Server'
                        message['response'] = 'error'
                        message['content'] =    ('Error. '
                                                'Invalid request or server malfunction. '
                                                'Please try again.')
                        self.connection.send(json.dumps(message))
                else:
                    # User is not logged in
                    if request == 'login':
                        # Login requested
                        message['response'] = 'info'
                        valid = username_validation(content)
                        if valid == 1:
                            # Login success
                            username = content
                            users.append(username)
                            message['sender'] = 'Server'
                            message['content']  = 'Login successful'
                            self.connection.send(json.dumps(message))
                            print msg_log
                            # Send history
                            message['response'] = 'history'
                            message['content'] = msg_log
                            self.connection.send(json.dumps(message))

                        elif valid == 2:
                            # Login unsuccessful - Invalid username
                            message['sender'] = 'Server'
                            message['content']  = 'Invalid username'
                            self.connection.send(json.dumps(message))
                            
                        else:
                            # Login unsuccessful - Username already in use
                            message['sender'] = 'Server'
                            message['content']  = 'Username already in use'
                            self.connection.send(json.dumps(message))
                            
                    elif request == 'help':
                        # Help requested
                        message['sender'] = 'Server'
                        message['response'] = 'info'
                        message['content'] = ('The servers available requests are:\n'
                                                'login<username>    -log in with the given username\n'
                                                'logout             -log out\n'
                                                'msg<message>       -send message\n'
                                                'names              -list users in chat\n'
                                                'help               -view help text')
                        self.connection.send(json.dumps(message))
                        
                    else:
                        # Request unavailable
                        message['sender'] = 'Server'
                        message['response'] = 'error'
                        message['content'] = 'Error. Please log in'
                        self.connection.send(json.dumps(message))
                        # /close socket and thread
                    #OBS DONT DO THIS FOR LOGIN SUCCESSFUL!!!!!!!!!!!
                    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            else:
                # No new requests from user
                if (len(msg_log) - log_len) and username:
                    # New messages from other users
                    for i in range(len(msg_log) - log_len):
                        self.connection.send(msg_log[log_len + i])
                    log_len = len(msg_log)
            
class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
