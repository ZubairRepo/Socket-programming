import socket
import os

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000
DOWNLOAD_PATH = '/download'  # Define the path to trigger the download
FILE_PATH = './index.html'  # Path to the file to be downloaded

# Create the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:
    # Wait for client connections
    client_socket, client_address = server_socket.accept()

    # Get the client request
    client_request = client_socket.recv(1024).decode()
    print(client_request)

    if DOWNLOAD_PATH in client_request:
        # If the request contains the download path, serve the file for download
        if os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'rb') as file:
                file_content = file.read()
                response = 'HTTP/1.0 200 OK\nContent-Disposition: attachment; filename="index.html"\nContent-Type: application/octet-stream\n\n'.encode() + file_content
        else:
            response = 'HTTP/1.0 404 Not Found\n\nFile not found'.encode()
    else:
        # Get the content of the requested resource (e.g., htdocs/index.html)
        resource_content = open(FILE_PATH, 'rb').read()
        response = 'HTTP/1.0 200 OK\n\n'.encode() + resource_content

    # Send the response to the client
    client_socket.sendall(response)
    client_socket.close()

# Close the socket
server_socket.close()
