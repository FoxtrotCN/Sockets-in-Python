import socket
import threading

username = input("Provide your username: ")
HOST = '127.0.0.1'
PORT = 55555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def receive_messages():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "@username":
                client.send(username.encode("utf-8"))
            else:
                print(message)

        except:
            print("An error occured.")
            client.close()
            break


def write_messages():
    while True:
        message = f"{username}: {input('> ')}"
        client.send(message.encode("utf-8"))


receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()


write_thread = threading.Thread(target=write_messages)
write_thread.start()


