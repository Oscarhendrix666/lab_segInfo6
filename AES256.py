from numpy import pad
from Crypto.Cipher import AES

def aes_encrypt_and_send(data, key, client_socket):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = cipher.iv

    # Enviar el IV y el ciphertext al cliente
    client_socket.send(iv + ciphertext)