import os
import socket
import time

# Create a socket.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.10.6', 22222))
server_socket.listen(5)
print("Host Name: ", server_socket.getsockname())

# Accept incoming connection.
client_socket, client_address = server_socket.accept()

# Get file details from the user.
file_name = input('Enter the file name: ')
file_size = os.path.getsize(file_name)

# Send file name and details to the client.
client_socket.send(f"{file_name + '__break_here__' + str(file_size)}".encode())

# Open the file and send its data.
with open(file_name, "rb") as file:
    # Start measuring the transfer time.
    start_time = time.time()
    while True:
        data = file.read(1024)
        if not data:
            break
        client_socket.sendall(data)
    # End measuring the transfer time.
    end_time = time.time()

print("File Transfer Complete. Time taken:", end_time - start_time)

# Close the server socket.
server_socket.close()
