import socket
import sys
import select

host= socket.gethostname()
SERVADR = (host, 6000)
IP= socket.gethostbyname(host)

class Server():
    def __init__(self):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.bind(SERVADR)

    def run(self):
        self.__s.listen()
        while True:
            client, addr = self.__s.accept()
            try:
                data= self._rec(client)
                print(data.decode())
                client.sendall(data)
                print('Sendall succesful')
                client.close()
                sys.exit()
            except SyntaxError:
                print('Error')

    def _rec(self, client):
        chunks= []
        fin= False
        print('Retreiving data')
        while not fin:
            print('Server retreival loop')
            client.settimeout(3)
            try:
                data= client.recv(32)
            except:
                data = b''
                print('Client socket timed out')
                pass
            print('Data:', data)
            chunks.append(data)
            fin = data == b''
        print('All data succesfully retreived')
        return b''.join(chunks)

class Client():
    def __init__(self, message):
        self.__message= message
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        try:
            print('Connecting')
            self.__s.connect(SERVADR)
            print('Connected', SERVADR)
            self._send()
            print('Received:', self._rec().decode())
            self.__s.close()
        except SyntaxError:
            print('Error')

    def _send(self):
        print('Sending')
        totalsent= 0
        msg = self.__message.encode()
        print(msg)
        try:
            while totalsent < len(msg):
                sent= self.__s.send(msg[totalsent:])
                totalsent += sent
            print('message sent')
        except SyntaxError:
            print('Error')

    def _rec(self):
        chunks = []
        finished= False
        print('Receiving')
        while not finished:
            print('loop')
            data = self.__s.recv(32)
            chunks.append(data)
            finished = data == b''
        print('Message received')
        return b''.join(chunks)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'server':
        print('Server!')
        Server().run()
    elif len(sys.argv) == 3 and sys.argv[1] == 'client':
        print('Client!')
        Client(sys.argv[2]).run()
    else:
        print('On se trouve dans le else')
