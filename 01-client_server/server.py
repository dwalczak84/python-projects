import socket             # Import socket module
import os

def server_example(host, port, new_file, b_size):

    s = socket.socket()         # Create a socket object
    s.bind((host, port))        # Bind to the port
    f = open(new_file, 'wb')    # open in binary

    s.listen(5)                 # Now wait for client connection.

    while True:
        c, addr = s.accept()     # Establish connection with client.
        print 'Got connection from', addr
        print "Receiving..."
        buf = c.recv(b_size)
        while (buf):
            f.write(buf)
            buf = c.recv(b_size)
        f.close()
        print "Done Receiving"
        c.send('Thank you for connecting')
        c.close()                # Close the connection
        return                   


# Input data and SERVER function call
host = '127.0.0.1'
port = 1234
new_file = 'operations_recv.txt'
b_size = 2000 * 1024

server_example(host, port, new_file, b_size)
