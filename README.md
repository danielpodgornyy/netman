# Netman
Netman is an application that is meant to show off many networking concepts through a collection of mini-to-medium sized projects. There is currently only one project implemented: the multiroom chat application

The applications are built soley with python, using the tkinter library as a framework for the GUI components. All other components are built with mostly vanilla python, including the server and HTTP request sender and handler components

---

## Table of Contents

- [Usage](#usage)
- [Project Descriptions](#project-descriptions)
    - [Chat](#chat)

## Usage

Before running the application, you must: 
- pull the required modules from the requirements document
- set a port number as an environmental variable named PORT

<br>

The client side of the application contains most of the functionality that the projects will require. To run this side of the application, you move into the client directory and run the following line in your terminal:

```
    python MainApp.py 
```

The server side of this application is currently only used by the chat project. The chat project REQUIRES for the server to be running. It can be ran on a seperate machine or the same machine as the client as long as you know the IP address of the server. In the server directory, run the following line in your terminal:

```
    python main.py
```

## Project Descriptions

### Chat:
The chat application allows you to speak with other people anonymously behind an input username once you connect to a server. A server contains multiple chat rooms where any user can create a new one that anyone can join. None of the chat room data including rooms or messages sent to each room is persisted so once the server shuts off, all of that data is thrown out (This may change in a future update).

The server and client implementation is custom made utilizing only the base socket module. The server uses HTTP push and pull data from the client and server, with one exception to be elaborated on later. The HTTP sender and handler are also custom made f    python main.py


The server and client implementation is custom made utior the server with no external module used. As such, the HTTP sender and handlers are only used for JSON data.

Since data on each clients screen needs to be updated live, each client has a seperate thread to listen for connections from the server. Whenever a chat message or chat room is added on the server, this notification is broadcast to every client but the client who sent the request. This data is sent as pure JSON since all the client has to update the GUI's on the client side
