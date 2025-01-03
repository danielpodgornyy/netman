import json

class HTTPRequestHandler():
    def __init__(self, req_stream, res_stream, controller, address):
        self.req_stream = req_stream
        self.res_stream = res_stream
        self.method = ''
        self.path = ''
        self.parameter = ''
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
                404: 'Not found',
                409: 'Conflict',
                500: 'Internal Server Error'
                }

        self.controller = controller
        self.address = address

        self.handler()

    def handler(self):
        self.parse_stream()

        # Use the correct handler based on the method
        # Write the appropriate response messages in the method handlers
        valid_methods = ('GET', 'HEAD', 'POST', 'DELETE')
        if self.method in valid_methods:
            method_handler = getattr(self, f"handle_{self.method}")
            method_handler()
        else:
            # An invalid request was recieved
            self.write_response_line(400)
            self.write_response_headers()

        # Send the response to the client
        self.res_stream.flush() # Stream parser

    def parse_stream(self):
        # Parse request line
        request_line = self.req_stream.readline().decode().strip(' \r\n')
        self.method = request_line.split(' ')[0]

        # If the path line contains a parameter, include it
        path_line = request_line.split(' ')[1]
        colon_pos = path_line.find(':')

        if (colon_pos != -1):
            self.path = path_line[:colon_pos]
            self.parameter = path_line[colon_pos+1:]
        else:
            self.path = path_line

        # Parse headers
        line = self.req_stream.readline().decode().strip(' \r\n')
        while(line != ''):
            header = line.split(': ')
            self.headers[header[0]] = header[1]
            line = self.req_stream.readline().decode().strip(' \r\n')

        # Retrieve the rest as the body
        self.body = self.req_stream.readline().decode().strip(' \r\n')


    # Method handlers

    def handle_GET(self):
        match self.path:
            case '/chat':
                chat_list = self.controller.get_curr_chats()

                if chat_list:
                    chat_list_json = json.dumps(chat_list)

                    self.write_response_line(200)
                    self.write_response_headers()
                    self.write_response_body(chat_list_json)
                else:
                    self.write_response_line(404)
                    self.write_response_headers()

            case '/logs':
                # Get the chatroom logs from the room name stored in a parameter
                chat_logs = self.controller.get_chat_logs(self.parameter)

                if chat_logs:
                    chat_logs_json = json.dumps(chat_logs)

                    self.write_response_line(200)
                    self.write_response_headers()
                    self.write_response_body(chat_logs_json)
                else:
                    self.write_response_line(404)
                    self.write_response_headers()
            case _:
                self.write_response_line(404)
                self.write_response_headers()


    def handle_POST(self):
        match self.path:
            case '/username':
                # Pull the username from the json
                username = json.loads(self.body)['username']

                # Try to input username
                if self.controller.input_username(username, self.address):
                    # OK
                    self.write_response_line(200)
                else:
                    # CONFLICT
                    self.write_response_line(409)
            case '/chat':
                # Pull the username from the json
                chat_room_name = json.loads(self.body)['chat_room_name']
                username = json.loads(self.body)['username']

                # Try to input username
                if self.controller.add_chat(chat_room_name, username):
                    # OK
                    self.write_response_line(200)
                else:
                    # CONFLICT
                    self.write_response_line(409)

            case '/logs':

                # Pull the username from the json
                chat_log = json.loads(self.body)['chat_log']

                # Try to input username
                if self.controller.enter_log(chat_log):
                    # OK
                    self.write_response_line(200)
                else:
                    self.write_response_line(500)

            case _:
                # NOT FOUND
                self.write_response_line(404)

        self.write_response_headers()

    def handle_HEAD(self):
        match self.path:
            case '/':
                self.write_response_line(200)
            case _:
                self.write_response_line(404)

        self.write_response_headers()


    def handle_DELETE(self):
        match self.path:
            case '/username':
                # Pull the username from the json
                username = json.loads(self.body)['username']

                # Delete username
                self.controller.delete_username(username)
                self.write_response_line(200)
            case _:
                self.write_response_line(404)

        self.write_response_headers()

    # Writing the the stream

    def write_response_line(self, status_code):
        response_line = f'HTTP/1.1 {status_code} {self.HTTPStatus[status_code]}\r\n'
        self.res_stream.write(response_line.encode())

        # For logging purposes
        print('HTTP RESPONSE:')
        print(response_line.strip('\r\n'))

    def write_response_headers(self, *args, **kwargs):
        # Make a copy of the headers and update the appropriate values
        headers_copy = self.headers.copy()
        headers_copy.update(**kwargs)

        # Write the headers to the response stream
        response_line = '\r\n'.join(f'{key}: {value}' for key, value in headers_copy.items())
        self.res_stream.write(response_line.encode())

        # Empty line to define end of headers
        self.res_stream.write(b'\r\n\r\n')

        # For logging purposes
        print(response_line + '\n')


    # Made for uniformity
    def write_response_body(self, body):
        self.res_stream.write(body.encode())

        print(body + '\n')

