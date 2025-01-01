class HTTPRequestSender():
    def __init__(self, req_stream, res_stream, http_request_data):
        self.req_stream = req_stream
        self.res_stream = res_stream
        print(self.req_stream)
        print(self.res_stream)
        self.req_data = http_request_data
        self.response_code = ''
        self.body = ''

        print(http_request_data)

        self.sender()
        self.reciever()

    def sender(self):
        # Build the string from the input request data
        request_line = f'{self.req_data["method"]} {self.req_data["path"]} HTTP/1.1\r\n'

        # List out each header
        request_line += '\r\n'.join(f'{key}: {value}' for key, value in self.req_data['headers'].items())

        request_line += '\r\n\r\n' + self.req_data['body'] + '\r\n'

        print(request_line)

        try:
            # Write to the file object buffer and send it through the socket
            self.req_stream.write(request_line.encode())
            self.req_stream.flush()
        except Exception as e:
            print('Error during flush: ', e)

    def reciever(self):
        response_line = self.res_stream.readline().decode().strip(" \r\n")

        # Get the response code
        self.response_code = response_line.split(' ')[1]

        # Skip past the header lines
        while response_line != "":
            response_line = self.res_stream.readline().decode().strip(" \r\n")

        # Get the body
        self.body = self.res_stream.readline().decode().strip(" \r\n")
