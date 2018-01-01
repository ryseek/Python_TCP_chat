import asyncio


def run_server(host, port):
    class User:

        def __init__(self, transport, peername):
            self.user_transport = transport
            self.user_peername = peername
            self.user_name = None
            self.count = 0

    class ClientServerProtocol(asyncio.Protocol):
        active_transport = []
        active_users = []

        def connection_made(self, transport):
            self.peername = transport.get_extra_info('peername')
            print('New connection from {}'.format(self.peername))
            self.transport = transport
            self.data = b""

            user = User(self.transport, self.peername)
            self.active_users.append(user)

            self.active_transport.append((self.transport, self.peername))

            str = "\nMicro chat V1 by ryseek and kupreeva \n"
            self.transport.write(str.encode())
            self.transport.write('What is your name?\n'.encode())

            # str = "joined our group \n"
            # self.process_data(str)

        def connection_lost(self, exc):
            str = "left our group \n"
            self.process_data(str)

            for element in self.active_transport:
                if element[0] == self.transport:
                    self.active_transport.remove(element)
                    print('Close connection from {}'.format(self.peername))

            for user in self.active_users:
                if user.user_transport == self.transport:
                    self.active_users.remove(user)

        def data_received(self, data):
            if self.data:
                data = self.data + data
                self.data = b""
            self.process_data(data.decode('utf-8'))

        def process_data(self, data):
            perenos = data[len(data)-1:len(data)]
            if perenos == "\r" or perenos == "\n":
                data = data[:len(data)-1]
            perenos = data[len(data) - 1:len(data)]
            if perenos == "\r" or perenos == "\n":
                data = data[:len(data) - 1]

            userName = ''
            for user in self.active_users:
                # проверяем, кто пишет сообщение
                if user.user_transport == self.transport:
                    user.count = user.count + 1
                    if user.count == 1:
                        user.user_name = data
                        print(self.peername)
                        print(user.user_name)
                    userName = user.user_name

            for user in self.active_users:
                if user.user_transport != self.transport:
                    str = "[{}]: ".format(userName) + data + "\n"
                else:
                    str = ">>"
                user.user_transport.write(str.encode())

            """
            for element in self.active_transport:
                # str = "[{}]: ".format(element[1][1]) + data + "\n"
                str = "[{}]: ".format(user.user_name) + data + "\n"
                if element[0] != self.transport:
                    element[0].write(str.encode())
                else:
                    str = ">>"
                    element[0].write(str.encode())"""


    loop = asyncio.get_event_loop()
    coro = loop.create_server(ClientServerProtocol, host, port)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


run_server("192.168.31.253", 8888) # enter your ip adress here