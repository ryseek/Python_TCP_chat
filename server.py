import asyncio


def run_server(host, port):

    class ClientServerProtocol(asyncio.Protocol):
        active_transport = []

        def connection_made(self, transport):
            self.peername = transport.get_extra_info('peername')
            print('New connection from {}'.format(self.peername))
            self.transport = transport
            self.data = b""

            self.active_transport.append((self.transport, self.peername))

            str = "\nMicro chat V1 by ryseek and kupreeva \n"
            self.transport.write(str.encode())

            str = "joined our group \n"

            self.process_data(str)

        def connection_lost(self, exc):
            str = "left our group \n"

            self.process_data(str)

            for element in self.active_transport:
                if element[0] == self.transport:
                    self.active_transport.remove(element)
                    print('Close connection from {}'.format(self.peername))

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

            for element in self.active_transport:
                str = "[{}]: ".format(element[1][1]) + data + "\n"
                if element[0] != self.transport:
                    element[0].write(str.encode())
                else:
                    str = ">>"
                    element[0].write(str.encode())


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

run_server("192.168.31.99", 8888) # enter your ip adress here