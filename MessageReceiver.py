# -*- coding: utf-8 -*-
from threading import Thread
#from MessageParser import MessageParser
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
       # self.Parser = MessageParser()
        self.client = client

        # TODO: Finish initialization of MessageReceiver
        
    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads
        runReceiver = True
        while runReceiver == True:
            payload = self.connection.recv(4096)
            #print "payload: ", payload, "end"
            if payload == -1:
                print "Payload -1"
                self.client.disconnect()
                exit
            if payload == '':
                print "Receiver thread shutdown"
                runReceiver = False
            else:
                message = json.loads(payload)
                print message['content']

