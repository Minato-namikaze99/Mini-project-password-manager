import random 
import math
import prime


def extended_gcd(a, b): # Helper function for the Extended Euclidean Algorithm
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def find_d(e, phi): # Finds d such that (d * e) % phi == 1
    g, x, y = extended_gcd(e, phi)
    if g != 1:
        raise ValueError("Modular inverse does not exist")
    else:
        return x % phi

p,q = prime.gen_prime(), prime.gen_prime()
#generates 2 prime numbers P and Q

while p==q: #if both the prime numbers generated are same, then generate again
    q = prime.gen_prime()

n = p*q 

phi_n = (p-1)*(q-1)

e = 2

while math.gcd(e, phi_n)!=1 : #checks if they are co prime or not, if not, regenerate e
    e+=1

k=2
d = find_d(e, phi_n)

print("Public Key:", n)
print("Private Key:", d)
print("Phi_n:",phi_n)
print("e:",e)
print("n:", n)
print("p:", p)
print("q:", q)

message = input("\n\nEnter a message to be encypted: ")

#encryption begins from here
message_ascii = [ord(c) for c in message] #this converts the message to its ASCII codes

# formula for encyption: (m^e)mod n = c
cipher = [pow(c, e, n) for c in message_ascii]
#this is the encrypted string

print("\n\nEncrypted Message:", cipher) #this can be saved on a bin file and shared


#decryption begins from here
message_enc = [pow(ch, d, n) for ch in cipher] #this is the decrypted string, i.e., currently its now a series of ASCII Codes

decr = "".join(chr(ch) for ch in message_enc) #this is the actual message after being converted from ASCII

print("\n\n\n\nDecrypted Message: ", decr)
