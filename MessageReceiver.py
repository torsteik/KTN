# -*- coding: utf-8 -*-
from threading import Thread
import Parser
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
            if payload == '':
                print "Receiver thread shutdown"
                runReceiver = False
            else:
                if json.loads(payload)['response'] == 'history':
                    self.client.isLoggedin = True
                print Parser.parse_json(payload, self.client.username)


