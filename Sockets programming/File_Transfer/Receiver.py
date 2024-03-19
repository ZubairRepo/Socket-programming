import os
import socket
import time

# Define the target host and port.
target_host = '192.168.10.6'
target_port = 22222

# Create a socket object.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try to connect to the socket.
try:
    client_socket.connect((target_host, target_port))
    print("Connected Successfully")
except Exception as e:
    print("Unable to connect:", e)
    exit(0)

# Receive file details from the server.
file_details = client_socket.recv(1024).decode()
file_name, file_size = file_details.split('_break_here_')

print("Received File Details:")
print("File Name:", file_name)
print("File Size:", file_size)

# Open and write the received file.
with open("./received_files/" + file_name, "wb") as received_file:
    # Start the timer.
    start_time = time.time()

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        received_file.write(data)

    # Stop the timer.
    end_time = time.time()

print('File received in: {:.5f} seconds'.format(end_time - start_time))
print("File transfer complete")

# Close the socket.
client_socket.close()
