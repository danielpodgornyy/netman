import os
from dotenv import load_dotenv, dotenv_values

from ChatServer import ChatServer
from utils.HTTPRequestHandler import HTTPRequestHandler

load_dotenv()

if __name__ == '__main__':
    ip_address = ''
    port = int(os.getenv('PORT'))
    http_server = ChatServer((ip_address, port), HTTPRequestHandler)

    http_server.start_server()

