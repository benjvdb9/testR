import socket 

class EchoServer():
    def __init__(self):
        self.__host = socket.gethostname() 
        self.__port = 6000 
        self.__size = 16
        self.__client= ''
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.__s.bind((self.__host, self.__port))

    def run(self):
        self.__s.listen()
        print('1')
        while 1:
            print('2')
            client, address = self.__s.accept()
            print('3')
            self.__client = client
            print('4')
            msg = self._rec()
            print(msg.decode())
            self.__client.close()

    def _rec(self):
        print('V1')
        data = self.__client.recv(self.__size)
        print('V2')
        if data:
            print('V3')
            print(data)
            self.__client.send(data)
            print('V4')
        else:
            print(data)
        return data

class EchoClient():
    def __init__(self, message):
        self.__host = socket.gethostname()
        self.__msg = message
        self.__port = 6000 
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.connect((self.__host, self.__port))

    def run(self):
        print('1')
        self.__s.send(self.__msg.encode())
        print('2')
        #data = self.__s.recv(16)          # Tous deux fonctionent 
        data = self._rec()                 #
        self.__s.close()
        print('Received:', data.decode())

    def _rec(self):
        finished = False
        chunks = []
        while not finished:
            data = self.__s.recv(16)
            print(data)
            chunks += [data]
            finished = data == b''
        print(chunks)
        return b''.join(chunks)

Res = input('Client/Server?')

if Res == 'server':
    EchoServer().run()
if Res == 'client':
    msg = input('Message?')
    EchoClient(msg).run()
    pass
