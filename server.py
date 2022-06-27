# echo-server.py


import socket
import os.path
from _thread import *
import threading
import time

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 80  # Port to listen on (non-privileged ports are > 1023)

q = []
def handle_client(conn,addr):

    while True:
        
        # data received from client
        data = conn.recv(2048)
        if not data:
            break
        request_string = data.decode('UTF-8')
        # q.append(request_string)
        # print(request_string)
        # time.sleep(2) #timeout
        
    # for i in q:
        input_arr = request_string.split(' ',2)
        command = input_arr[0]
        filee = input_arr[1]
        filename = filee.replace("/","")
        version = input_arr[2]
        version_split = version.split('\r\n\r\n')
        if command == 'GET':
            if not os.path.exists(filename):
                    error = 'HTTP/1.1 404 Not Found\r\n\r\n'
                    error_packet = bytes(error,'utf-8')
                    conn.sendall(error_packet)
            else:
                    f = open(filename,"r",encoding="utf-8", errors='ignore')
                    body = f.read()
                    response = send_http_response_get(body)
                    response_packet = bytes(response, 'utf-8')
                    conn.sendall(response_packet)
        else:
            body = version_split[1]
            bodyy = body.replace("\r\n","")
            f = open(filename,'a')
            f.write(bodyy)
            f.write('\n')
            f.close()
            response = send_http_response_post()
            response_packet = bytes(response, 'utf-8')
            conn.sendall(response_packet)

        time.sleep(3)
    #close connection after sending responses    
    conn.close()

def send_http_response_get(body):
    response_pack = 'HTTP/1.1 200 OK\r\n\r\n' + body + '\r\n'
    return response_pack

def send_http_response_post():
    response_pack = 'HTTP/1.1 200 OK\r\n'
    return response_pack

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))

    s.listen()
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()
