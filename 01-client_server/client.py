import socket               # Import socket module
import os

def client_example(host, port, file_to_send, b_size):

    #get file size
    statinfo = os.stat(file_to_send)
    file_size = statinfo.st_size
    f = open(file_to_send, 'rt') #open in binary
    total_sent = 0

    #open connection to server
    s = socket.socket()
    s.connect((host, port))

    while (total_sent < file_size):
	print 'Sending...'
	buf = f.read(b_size)
        sent = s.send(buf)
        #jesli funkcja send zwroci 0 bajtow to oznacza ze error - np zerwane polaczenie, brak sieci, serwer zdechl, itp
        if sent == 0:
		raise RuntimeError("socket connection broken")
        total_sent = total_sent + sent; 

    f.close()
    print "Done Sending"
    s.shutdown(socket.SHUT_WR)
    print s.recv(b_size)
    s.close()                     # Close the socket when done
    return

# Input data and CLIENT function call
host = '127.0.0.1'
port = 1234
file_to_send = 'operations.txt'
b_size = 20000 * 1024

client_example(host, port, file_to_send, b_size)
