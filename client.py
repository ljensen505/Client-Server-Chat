"""
Lucas Jensen
CS372 Portfolio Project
Chat Client
"""

import socket
from server import PORT, HOST, BUFFER, FORMAT, get_msg, give_instructions

"""
Two resources:
- https://docs.python.org/3.4/howto/sockets.html
- my previous http server in this class
"""


class Client:
    def __init__(self):
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect((HOST, PORT))
        print(f"Connected to: {HOST} on port: {PORT}")
        print("===> Currently in Chat mode. Enter 'hangman' without the quotations to play Hangman!")
        print("===> To return to chat mode, enter 'chat'")

    def chat(self):
        give_instructions()

        connected = True
        while connected:
            msg = get_msg()

            self._client.sendall(bytes(str(msg), encoding=FORMAT))
            res = self._client.recv(BUFFER).decode(FORMAT)

            if res == '/q':
                # echo quit message so the server also quits
                self._client.sendall(bytes('/q', encoding=FORMAT))
                connected = False
                continue

            print(f"{res}")

        self._client.close()


if __name__ == "__main__":
    client = Client()
    client.chat()
