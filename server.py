import socket
import threading

SERVER="0.0.0.0"
PORT=1234
CLIENTS=[]


def client_listen(conn,addr):
    message=""
    while True:
        message+=conn.recv(2048).decode()
        if not message:
            print(f"{addr[0]} has disconnected")
            CLIENTS.remove(conn)
            break
        else:
            if message[-1]=="\n":
                resp=addr[0]+": "+message
                print(resp)
                broadcast(resp)
                message=""
            


def broadcast(message):
    for client in CLIENTS:
        try:
            client.sendall(message.encode())
        except:
            CLIENTS.remove(client)


def main():
    print("Waiting.....")
    global CLIENTS
    sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    sock.bind((SERVER, PORT))

    while True:
        sock.listen(100)
        conn,addr=sock.accept()
        CLIENTS.append(conn)
        i=threading.Thread(target=client_listen,args=(conn,addr,))
        i.start()
main()
