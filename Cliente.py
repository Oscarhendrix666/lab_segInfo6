from http import client
import random
import socket
import pickle
import RSA


def cliente():
    socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_cliente.connect(('127.0.0.1', 800))

    q = int(input("Ingresa tu clave numerica: "))

    socket_cliente.sendall(str(q).encode())

    serie =socket_cliente.recv(4096)
    valores_server = pickle.loads(serie)

    #obtener valores publicos
    n = valores_server["n"]
    phi_N = valores_server["phi_N"]
    e = valores_server["e"]

    print(f"clave publica: {n,e}")

    try:
        d = RSA.find_mod_inv(e, phi_N) #valor de la llave privada (d)
        print('proceso realizado exitoso')

    except:
        print('El valor del inverso no existe.\n')

    msg = input("mensaje a enviar: ")
    enc_msg = RSA.cifrar(msg, e, n)

    with open('mensaje_entrada.txt', 'w') as file:
        file.write(str(enc_msg))

    print("Mensaje cifrado guardado en mensaje_cifrado.txt")

    # Enviar el archivo cifrado al servidor
    with open('mensaje_cifrado.txt', 'rb') as file:
        file_data = file.read()
        socket_cliente.sendall(file_data)

    print("Archivo cifrado enviado al servidor.")

    # Descifrar el mensaje
    file_data = socket_cliente.recv(4096)

    # Recibir respuesta del servidor y decodificarlo
    with open('mensaje_recibido.txt', 'rb') as file:
        mensaje_cifrado = int(file.read())


    mensaje_descifrado = RSA.descifrar(mensaje_cifrado, d, n)
    # Guardar el archivo cifrado
    with open('mensaje_recibido.txt', 'wb') as file:
        file.write(mensaje_descifrado)

    print("Mensaje descifrado")

    socket_cliente.close()


    print('Comunicacion con el gamal\n')
    g = random.randint(1, 1000)
    a = 369 #clave privada del emisor
    b = 693 #clave privada del receptor
    k = (g**a) % p
    clave_publica = (g, p, k)
    print(f'se genero la siguiente clave publica: {clave_publica}')
    m = int(input('ingresar el mensaje que desea enviar--> '))
    #cifrando
    y1 = (g**b) % p
    y2 = ((k**b) * m) % p
    #descifrando
    m2 = (y1**(p-1-a) * y2) % p
    print(f'El mensaje descifrado es el siguiente: {m2}\n')

cliente()