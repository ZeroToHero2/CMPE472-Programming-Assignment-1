# Import socket module
from socket import *
import sys  # In order to terminate the program
# Create a TCP server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)
serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 8080  # Use any port number you like
# Bind the socket to a public host, and a port
serverSocket.bind(('', serverPort))
serverSocket.listen(1)  # Maximum number of connections is 1

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()

    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        # Send one HTTP header line into socket
        connectionSocket.send(
            "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n".encode())

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    except IOError:
        # Send response message for file not found
        connectionSocket.send(
            "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n".encode())
        connectionSocket.send(
            "<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())

        # Close client socket
        connectionSocket.close()

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
