import RSA
import socket
import pickle

def send_values(connection, n, phi_N,e):
    values_to_send = {"n": n, "phi_N": phi_N,"e": e}
    serialized_values = pickle.dumps(values_to_send)
    connection.sendall(serialized_values)

def Servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 800))
    server.listen(1)

    print("Servidor esperando conexión")

    conn, Address = server.accept()

    print(f"Conexión establecida desde: {Address}")

    p = 863

    q = int(conn.recv(4096).decode())

    n = RSA.generarN(p,q)
    phi_N = RSA.genPhi_N(p,q)
    e = RSA.generaE(phi_N)

    send_values(conn, n, phi_N, e)

    server.close()

Servidor()