#!/usr/bin/env python3
import socket
import time
import sys
import requests

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

def main():

    
    host = 'www.google.com'
    port = 80
    
    #create a TCP socket as proxy_start
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start:
    
        #to reuse the same bind port
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        proxy_start.bind((HOST, PORT))
        #set to listening mode
        proxy_start.listen(1)
        
        #continuously listen for connections
        while True:
            #specify a proxy start
            conn, addr = proxy_start.accept()
            print("Connected by", addr)

            #to connect to google
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end:
                remote_ip = get_remote_ip(host)
                proxy_end.connect((remote_ip , port))
                print (f'Socket Connected to {host} on ip {remote_ip}')


                #recieve data, wait a bit, then send it back
                full_data = conn.recv(BUFFER_SIZE)
                proxy_end.sendall(full_data)

                #shut down
                proxy_end.shutdown(socket.SHUT_WR)

                #send data to original connection - step 7
                full_data = proxy_end.recv(BUFFER_SIZE)
                r = requests.post("https://www.google.com/", full_data)
                response = r.text
                conn.sendall(response.encode())
            conn.close()

if __name__ == "__main__":
    main()
