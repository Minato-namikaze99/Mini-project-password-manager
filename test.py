import random
import math

def is_prime(n, k=5):
    """Rabin-Miller primality test."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Write n - 1 as (2^s) * d
    s = 0
    d = n - 1
    while d % 2 == 0:
        d //= 2
        s += 1

    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def mod_inverse(e, phi): #finds the mod inverse 
    for d in range(3, phi):
        if (d*e)%phi==1:
            return d 
    
    raise ValueError("Mod_Inverse does not exist")

def generate_prime(min_value, max_value):
    """Generate a prime number using Rabin-Miller test."""
    while True:
        prime = random.randint(min_value, max_value)
        if is_prime(prime):
            return prime

# Example usage:
min_value = 1000
max_value = 5000
p,q = generate_prime(min_value, max_value), generate_prime(min_value, max_value) 
while p==q: #if both the prime numbers generated are same, then generate again
    q = generate_prime(1000, 5000)

n = p*q 

phi_n = (p-1)*(q-1)

e = random.randint(3, phi_n) 

while math.gcd(e, phi_n)!=1 : #checks if they are co prime or not, if not, regenerate e
    e = random.randint(3, phi_n) 

d = mod_inverse(e, phi_n)

print("Public Key:", e)
print("Private Key:", d)
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