# -*- coding: utf-8 -*-
from threading import Thread
import json
import time

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """
        Thread.__init__(self)
        self.daemon = True
        self.connection = connection
        self.client = client

        
    def run(self):
        runReceiver = True
        while runReceiver == True:
            payload = self.connection.recv(4096)
            message = payload
            
            ## Hvis recv ikke klarer å hente hele meldingen i en runde
            while len(payload) == 4096:
                payload = self.connection.recv(4096)
                print "LEN: " +  str(len(payload))
                message += payload
                
            if message == '':
                print "Receiver thread shutdown"
                runReceiver = False
            else:
                if json.loads(message)['response'] == 'history':
                    self.client.isLoggedin = True
                print self.parse_json(message, self.client.username)
                
    def parse_json(self, string, username):
        obj = json.loads(string)
        ret_val = ''
        if obj['response'] == 'error':
            ret_val = '\n'
            ret_val += '*****\tERROR\t*****\n'
            ret_val += obj['sender'] + ': '
            ret_val += obj['content']
            ret_val += '\n'
            return ret_val
        elif obj['response'] == 'message':
            ret_val += '\n'
            ret_val += obj['sender'] + ': '
            ret_val += obj['content']
            ret_val += '\n'
            if obj['sender'] == username:
                return ''
            return ret_val
        elif obj['response'] == 'history':
            #print obj['content'][0]
            ret_val = '\n*******************************'
            ret_val += '\nPreviously on ' + obj['sender'] + "'s server:\n"
            for jobj in obj['content']:
                ret_val += self.parse_json(jobj, '')
            ret_val += '*******************************\n'
            return ret_val
        elif obj['response'] == 'info':
            ret_val = '\n'
            ret_val += '*****\tINFO\t*****\n'
            ret_val += obj['sender'] + ': '
            ret_val += obj['content']
            ret_val += '\n'
            return ret_val
        else:
            return '\n\nInvalid Response: "' + obj['response'] + '"\n\n'
