from http import client
import random
import socket
import pickle
import RSA
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def comprobarClave(k1,k2):
    if k1 == k2:
        return True
    else:
        return "La clave no coincide"

def aes_receive_and_decrypt(key, server_socket):
    # Recibir el IV y el ciphertext del cliente
    data = server_socket.recv(1024)
    
    # Extraer el IV y el ciphertext
    iv = data[:AES.block_size]
    ciphertext = data[AES.block_size:]

    # Crear un objeto AES para desencriptar
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Desencriptar el ciphertext y quitar el relleno
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)

    return decrypted_data.decode()

def calcular_md5(archivo):
    hash_md5 = hashlib.md5()
    with open(archivo, "rb") as f:
        for bloque in iter(lambda: f.read(4096), b""):
            hash_md5.update(bloque)
    return hash_md5.hexdigest()

def cliente():
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_cliente.connect(('127.0.0.1', 800))
    serie =socket_cliente.recv(4096)
    valores_server = pickle.loads(serie)

    #obtener valores publicos
    n = valores_server["n"]
    phi_N = valores_server["phi_N"]
    e = valores_server["e"]

    try:
        d = RSA.find_mod_inv(e, phi_N) #valor de la llave privada (d)
        print('proceso realizado exitoso')

    except:
        print('El valor del inverso no existe.\n')

    print(f"clave publica: {n,e}")

    msg = 15478851321
    enc_msg = RSA.cifrar(msg, e, n)

    with open('mensaje de entrada.txt', 'w') as file:
        file.write(str(enc_msg))
    file = 'mensaje de entrada.txt'
    print("Mensaje cifrado guardado en mensaje de entrada.txt")
    socket_cliente.send(file)
    print("Archivo cifrado enviado al servidor.")

    # Actividad 2
    p = 757
    g = 547

    b = 382
    Bc = int((g**b)%p)
    socket_cliente.send(Bc)
    As = socket_cliente.recv(4096)
    kb = int((As**b)%p)
    socket_cliente.send(kb)
    if comprobarClave(ka,Kb) == True:
        dec_msg = aes_receive_and_decrypt(key=kb, server_socket=socket_cliente)
        with open('mensaje de vuelta.txt', 'w') as file:
            file.write(str(dec_msg))
    else:
        "Ha ocurrido un error"

    md5_send = calcular_md5(archivo='mensaje de vuelta.txt')
    print(f"md5 de archivo desencriptado recibido: {md5_send}")
    socket_cliente.close()

cliente()