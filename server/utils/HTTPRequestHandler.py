import json

class HTTPRequestHandler():
    def __init__(self, req_stream, res_stream, controller):
        self.req_stream = req_stream
        self.res_stream = res_stream
        self.method = ''
        self.path = ''
        self.protocol = ''
        self.headers =  {
                'Content-Type': 'application/json',
                'Content-Length': '0',
                'Connection': 'close'
                }
        self.body = ''

        # Only the necessary codes I'll need
        self.HTTPStatus = {
                200: 'OK',
                400: 'Bad Request',
                404: 'Not found'
                }

        self.controller = controller

        self.handler()

    def handler(self):
        self.parse_stream()

        valid_methods = ('GET', 'HEAD', 'POST')
        if self.method in valid_methods:
            method_handler = getattr(self, f"handle_{self.method}")
            method_handler()
        else:
            # An invalid request was recieved
            self.write_response_line(400)
            self.write_response_headers()

    def parse_stream(self):
        # Parse request line
        request_line = self.req_stream.readline().decode().strip(' \r\n')
        self.method = request_line.split(' ')[0]
        self.path = request_line.split(' ')[1]
        print(request_line, self.method, self.path)

        # Parse headers
        line = self.req_stream.readline().decode().strip(' \r\n')
        while(line != ''):
            header = line.split(': ')
            self.headers[header[0]] = header[1]
            line = self.req_stream.readline().decode().strip(' \r\n')

        # Retrieve the rest as the body
        self.body = self.req_stream.readline().decode().strip(' \r\n')

    def handle_GET(self):
        match self.path:
            case '/':
                pass
            case _:
                self.write_response_line(404)
                self.write_response_headers()

    def handle_POST(self):
        match self.path:
            case '/username':
                # Pull the username from the json
                username = json.loads(self.body)['username']

                self.controller.input_username(username)
            case _:
                self.write_response_line(404)
                self.write_response_headers()

    def handle_HEAD(self):
        match self.path:
            case '/username':
                pass
                # pull username from db
            case _:
                self.write_response_line(404)
                self.write_response_headers()

    def write_response_line(self, status_code):
        response_line = f'HTTP/1.1 {status_code} {self.HTTPStatus[status_code]}\r\n'
        self.res_stream.write(response_line.encode())

        print(response_line)

    def write_response_headers(self, *args, **kwargs):
        # Make a copy of the headers and update the appropriate values
        headers_copy = self.headers.copy()
        headers_copy.update(**kwargs)

        # Write the headers to the response stream
        response_line = '\r\n'.join(f'{key}: {value}' for key, value in headers_copy.items())
        self.res_stream.write(response_line.encode())

        # Empty line to define end of headers
        self.res_stream.write(b'\r\n\r\n')

        print(response_line)



