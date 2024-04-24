""" module: sendsignal
    file: sendsignal.py 
    application: Automated tool box inventory control system helper script
    language: python
    computer: ROG Flow Z13 GZ301ZE_GZ301ZE
    opertaing system: windows subsystem  ubuntu
    course: CPT_S 422
    team: Null Terminators
    author: Caitlyn Powers 
    date: 4/17/24
   """
import socket
import json

"""
    name:sendsignal 
    purpose: Send start signal to the automatedtoolbox program. 
    operation: Everything is hardcoded since this script was just made for testing. 
"""

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)



# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #print(f"Connected by {addr}")  # Step 1: Confirm connection establishment
    data = s.recv(1024)
    print(data)
    data_to_send = json.dumps({"toolbox": 0, "UserID": 11}).encode('utf-8')
    s.send(data_to_send)
   
        
        #data_to_send = json.dumps({"stop": "stop", "bool": True}).encode('utf-8')
        #s.send(data_to_send)
        
        

#print(f"Received {data!r}")
