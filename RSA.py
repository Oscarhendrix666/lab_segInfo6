import math
import random

def generarN(a, b):
    valor = a * b
    return valor

def genPhi_N(a,b):
    phi_n = (a-1)*(b-1)
    return phi_n

def e_value(phi_N):
    e = 0
    mcd = 0
    seguir = True
    while seguir:
        e = random.randint(phi_N/2,phi_N)
        mcd = math.gcd(e, phi_N)
        if mcd == 1:
            seguir = False
    return e

def find_mod_inv(a,m):
    for x in range(1,m):
        if((a%m)*(x%m) % m==1):
            return x
    raise Exception('El valor del inverso no existe.')

def cifrar(m, e, n):
    cifrado = (m**e) % n
    return cifrado

def descifrar(enc,d, n):
    descifrado = (enc**d) % n
    return descifrado