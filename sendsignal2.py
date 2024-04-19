import socket
import json
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)



# echo-client.py

import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #print(f"Connected by {addr}")  # Step 1: Confirm connection establishment
    #data_to_send = json.dumps({"toolbox": 0, "UserID": 0}).encode('utf-8')
    #s.send(data_to_send)
    #while True:
        
          # Step 5: Print received data
        #time.sleep(5)
        
    data_to_send = json.dumps({"stop": "stop", "bool": True}).encode('utf-8')
    s.send(data_to_send)
        
        

#print(f"Received {data!r}")
