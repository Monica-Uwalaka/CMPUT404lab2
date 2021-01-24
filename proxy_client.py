import socket
import sys



def main():
    try:
        host = 'localhost'
        port = 8001
        payload = 'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'
        buffer_size = 1024
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1' , port))
        print (f'Socket Connected to {host} on ip 127,\.0.0.1')

        #send the data and shutdown
        s.sendall(payload.encode())
        s.shutdown(socket.SHUT_WR)

        data = s.recv(buffer_size)
        print(data)
    except Exception as e:
        print(e)
    finally:
        #always close at the end!
        s.close()
    
if __name__ == "__main__":
    main()
