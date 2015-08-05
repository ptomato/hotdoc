# -*- coding: utf-8 -*-
#!/usr/bin/python

import zmq
import sys
import json
from datetime import datetime
from subprocess import Popen
from time import sleep
import os

class Converter (object):
    def __init__(self):
        self.context = zmq.Context()

        module_path = path = os.path.dirname(__file__)
        server_executable = os.path.join(module_path, "pandoc_server")
        self.server = Popen ([server_executable])
        #  Socket to talk to server
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")

    def convert (self, informat, outformat, payload):
        job = json.dumps ({'informat': informat,
                           'outformat': outformat,
                           'payload': payload})
        self.socket.send(job)
        result = self.socket.recv(copy=False)

        return (str(result)).decode('utf-8')

    def __del__ (self):
        self.server.terminate ()

pandoc_converter = Converter()

if __name__=="__main__":
    with open (sys.argv[1], 'r') as f:
        contents = f.read ()

    n = datetime.now ()
    out = pandoc_converter.convert (sys.argv[2], sys.argv[3], contents)
    print out