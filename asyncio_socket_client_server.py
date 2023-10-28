class AsyncPowerServer(object):
    def __init__(self):
        self.ip = Settings().POWER_IP
        self.port = Settings().POWER_PORT

    async def readable_handle(self, reader, writer):
        """
        获取客户端发送的数据
        """    
        # TODO: 根据message类型或者reader的id来绑定对应的处理函数并处理结果
        data = await reader.read(100)
        message = data.decode()
        addr = writer.get_extra_info('peername')
        print(f"Received {message!r} from {addr!r}")
        return message

    async def writeable_handle(self, writer, message):
        """
        数据处理和组装完成后返回给客户端
        """
        print(f"Send: {message!r}")
        writer.write(orjson.dumps(message).encode("utf-8"))
        await writer.drain()
        print("Close the connection")
        writer.close()

    async def data_handle(self, reader, writer):
        """
        数据处理入口
        """
        message = await self.readable_handle(reader, writer)
        await self.writeable_handle(writer, message)

    async def run(self):
        server = await asyncio.start_server(
            self.data_handle, self.ip, self.port)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()
