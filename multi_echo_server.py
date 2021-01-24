'''
citation
source : Real Python.com
URL: https://realpython.com/python-sockets/#multi-connection-server

'''

#!/usr/bin/env python3
import socket
import time
import socketserver
import selectors

#define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

sel = selectors.DefaultSelector()

def service_connection(key, mask):
    sock = key.fileobj
    data = key.data
    if mask & selectors.EVENT_READ:
        recv_data = sock.recv(1024)  # Should be ready to read
        if recv_data:
            data.outb += recv_data
        else:
            print('closing connection to', data.addr)
            sel.unregister(sock)
            sock.close()
    if mask & selectors.EVENT_WRITE:
        if data.outb:
            print('echoing', repr(data.outb), 'to', data.addr)
            sent = sock.send(data.outb)  # Should be ready to write
            data.outb = data.outb[sent:]



def accept(s):
    conn, addr = s.accept()
    print("Connected by", addr)

    conn.setblocking(False)
    data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
    events = selectors.EVENT_READ | selectors.EVENT_WRITE
    sel.register(conn, events, data=data)
    
    # #recieve data, wait a bit, then send it back
    # full_data = conn.recv(BUFFER_SIZE)
    # time.sleep(0.5)
    
    # conn.sendall(full_data)
    # conn.close()


def main():
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        #configure socket to non-blocking mode
        s.setblocking(False)
        sel.register(s, selectors.EVENT_READ, data=None)

        
        #continuously listen for connections
        while True:
            events = sel.select(timeout = None)
            for key, mask in events:
                if key.data is None:
                    accept(key.fileobj)
                else:
                    service_connection(key, mask)
            # conn, addr = s.accept()
            # print("Connected by", addr)
            
            # #recieve data, wait a bit, then send it back
            # full_data = conn.recv(BUFFER_SIZE)
            # time.sleep(0.5)
            
            # conn.sendall(full_data)
            # conn.close()

if __name__ == "__main__":
    main()
