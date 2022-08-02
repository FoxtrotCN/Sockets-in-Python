import socket
import threading

HOST = '127.0.0.1'
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen()
print(f"Server running on {HOST}: {PORT}")

clients = []
usernames = []


def broadcast(message, _client):
    for client in clients:
        if client != _client:
            client.send(message)


def handle_message(client):
    while True:

        try:
            message = client.recv(1024)
            broadcast(message, client)

        except:
            index = clients.index(client)
            username = usernames[index]
            broadcast(f"ChatBot: {username} disconnected.".encode("utf-8"))
            clients.remove(client)
            usernames.remove(username)
            client.close()


def receive_connections():
    while True:
        client, address = server.accept()
        client.send("@username".encode("utf-8"))
        username = client.recv(1024).decode("utf-8")

        clients.append(client)
        usernames.append(username)

        print(f"{username} is connected with {str(address)}")

        message = f"ChatBot: {username} is online".encode("utf-8")
        broadcast(message, client)
        client.send("Connected to the server".encode("utf-8"))

        thread = threading.Thread(target=handle_message, args=(client,))
        thread.start()


receive_connections()
