import RSA
import socket
import pickle
import hashlib
from numpy import pad
from Crypto.Cipher import AES

def send_values(connection, n, phi_N,e):
    values_to_send = {"n": n, "phi_N": phi_N,"e": e}
    serialized_values = pickle.dumps(values_to_send)
    connection.sendall(serialized_values)

def comprobarClave(k1,k2):
    if k1 == k2:
        return True
    else:
        return "La clave no coincide"

def aes_encrypt_and_send(data, key, client_socket):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = cipher.iv

    # Enviar el IV y el ciphertext al cliente
    client_socket.send(iv + ciphertext)

def calcular_md5(archivo):
    hash_md5 = hashlib.md5()
    with open(archivo, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            hash_md5.update(bloque)
    return hash_md5.hexdigest()

def Servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 800))
    server.listen(1)

    print("Servidor esperando conexión")

    conn, Address = server.accept()

    print(f"Conexión establecida desde: {Address}")

    #Actividad 1 - RSA
    p = 863
    q = 509

    n = RSA.generarN(p,q)
    phi_N = RSA.genPhi_N(p,q)
    e = RSA.generaE(phi_N)

    try:
        d = RSA.find_mod_inv(e, phi_N) #valor de la llave privada (d)
        print('proceso realizado exitoso')

    except:
        print('El valor del inverso no existe.\n')

    send_values(conn, n, phi_N, e)

    # Aqui server recibe mensaje encriptado y en consecuencia
    # Descifrar el mensaje recibido en el archivo
    file_data = server.recv(4096)
    # Recibir respuesta del cliete y decodificarlo
    with open(file_data, 'rb') as file:
        mensaje_cifrado = int(file.read())

    mensaje_descifrado = RSA.descifrar(mensaje_cifrado, d, n)
    # Guardar el archivo descifrado
    with open('mensaje de salida.txt', 'wb') as file:
        file.write(mensaje_descifrado)

    print("Mensaje de salidad guardado")

    #Desafio 2 diffie hellman with Aes256 cipher
    p = 757
    g = 547

    a = 109
    As = int((g**a)%p)
    server.send(As)
    Bc = server.recv(4096)
    ka = int((Bc**a)%p)
    Kb = server.recv(4096)

    if comprobarClave(ka,Kb) == True:
        aes_encrypt_and_send(data='mensaje de salida.txt', key=Kb, client_socket=conn)
    else:
        print("Algo no ha funcionado")


    md5_in = calcular_md5(archivo=file_data)
    md5_out = calcular_md5(archivo='mensaje de salida.txt')

    print(f"md5 de archivo encritado recibido: {md5_in}")
    print(f"md5 de archivo encritado con AES enviado: {md5_out}")
    server.close()

Servidor()
