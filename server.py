"""
Lucas Jensen
CS372 Portfolio Project
Chat Server
"""

import socket
from hangman import Hangman


"""
Three resources:
- https://docs.python.org/3.4/howto/sockets.html
- https://www.techwithtim.net/tutorials/socket-programming/
- my own previous HTTP server assignment for this class
"""

PORT = 8000
HOST = 'localhost'
BUFFER = 1024
FORMAT = 'utf-8'


class Server:
    def __init__(self):
        self._buffer = BUFFER
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((HOST, PORT))
        self._server.listen(5)
        print(f"Server listening on: {HOST} on port: {PORT}")
        self._client, self._addr = self._server.accept()
        self._need_instructions = True
        self._playing = False
        self._game = Hangman()

    def chat(self):
        print(f"Connected by {self._addr}")
        print("Waiting for message...")

        connected = True

        while connected:
            res = self._client.recv(BUFFER).decode(FORMAT)

            # check if res is quit message
            if res == '/q':
                # echo quit message so the client also quits
                self._client.sendall(bytes('/q', encoding=FORMAT))
                connected = False
                continue

            print(f"{res}")
            if self._playing:
                self._game.make_guess(res)

            if res == "hangman":
                print("Now playing Hangman!")
                self._playing = True
            elif res == 'chat':
                print("Now chatting")
                self._playing = False
                # reset the game
                self._game = Hangman()

            # this will only happen once
            if self._need_instructions:
                give_instructions()
                self._need_instructions = False

            if self._playing:
                if len(res) == 1 or res == 'hangman':
                    if self._game.get_status() == 'playing':
                        msg = self._game.get_board()
                    else:
                        msg = self._game.get_status()
                else:
                    msg = "Make a valid guess."
            else:
                msg = get_msg()

            self._client.sendall(bytes(msg, encoding=FORMAT))

        self._server.close()


def give_instructions():
    print("Type /q to quit")
    print("Enter message to send...")


def get_msg():
    while True:
        msg = input("> ")
        if msg != "":
            return msg
        print("Invalid message!")


if __name__ == "__main__":
    server = Server()
    server.chat()
