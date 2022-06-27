# echo-client.py

import socket
import codecs

def construct_http_request_packet(command,file_name,HOST,PORT):
    
        if command == 'GET':
           str = command + ' /' + file_name + ' HTTP/1.1\r\n' + 'Host:' + HOST + ':' + '80\r\n\r\n'
        if command == 'POST':
           
            if(file_name.endswith('.txt')):
                f = open(file_name,"r")
                body = f.read()
            elif(file_name.endswith('html')):
                f = codecs.open(file_name, "r", "utf-8")
                body = f.read()
            else:
               f = open(file_name, encoding="utf8", errors='ignore')
               body = f.read()
            f.close()
            str = command + ' /' + file_name + ' HTTP/1.1\r\n' + 'Host:' + HOST + ':' + '80\r\n\r\n' + body +'\r\n'
        return str

f = open("inputfile.txt", "r")
a = True
cache = {}
while a:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        x = f.readline()
        if not x:
            a = False
            continue
        input_arr = x.split()
        command = input_arr[0]
        file_name = input_arr[1]
        HOST = input_arr[2]
        arr_len = len(input_arr)
        if arr_len == 3:
           PORT = 80
           port_number = 80
        else:
           PORT = input_arr[3]
           port_number = int(PORT)
     
        strr = construct_http_request_packet(command,file_name,HOST,PORT)
        #caching
        if strr in cache:
            response_string = cache.get(strr)
            if command == 'GET':
                response_split = response_string.split('\r\n\r\n')
                if len(response_split) == 2:
                    body = response_split[1]
            print(response_string)
            continue
        
        s.connect((HOST, port_number))
        res = bytes(strr, 'utf-8')
        s.sendall(res)
        data = s.recv(2048)
        # s.close()
        if command == 'GET':
            response = data.decode('utf-8')
            response_arr = response.split('\r\n\r\n')
            if len(response_arr) == 2:
               body = response_arr[1]
               bodyy = body.replace("\r\n","")
               new_file = open(file_name, "a", newline='',encoding="utf-8")
               new_file.write(bodyy)
           
        else:
            response = data.decode('utf-8')
        cache[strr] = response
        s.close()
f.close()
