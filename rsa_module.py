import random
import math
import prime

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def find_d(e, phi):
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % phi

def keygen():
    p, q = prime.gen_prime(), prime.gen_prime()
    
    while p == q:
        q = prime.gen_prime()

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 2
    while math.gcd(e, phi_n) != 1:
        e += 1

    d = find_d(e, phi_n)
    l = [e,n,d]
    return l

def encrypt(public_key, plaintext):
    e, n = public_key
    message_ascii = [ord(c) for c in plaintext]
    cipher = [pow(c, e, n) for c in message_ascii]
    return cipher

def decrypt(private_key, public_key, ciphertext):
    d = private_key
    e, n = public_key
    message_enc = [pow(ch, d, n) for ch in ciphertext]
    decr = "".join(chr(ch) for ch in message_enc)
    return decr