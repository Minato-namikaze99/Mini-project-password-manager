import random 
import math
 
def is_prime(n): #checks whether a number is prime or not
    if n<2:
        return False
    
    for i in range(2, n//2 +1):
        if n%i==0:
            return False
        
    return True 

def generate_prime(min_value, max_value): #generates prime number between a range
    prime=random.randint(min_value, max_value)
    while not is_prime(prime): #if the number generated is not prime, redo it again
        prime=random.randint(min_value, max_value)

    return prime

def mod_inverse(e, phi): #finds the mod inverse 
    for d in range(3, phi):
        if (d*e)%phi==1:
            return d 
    
    raise ValueError("Mod_Inverse does not exist")

p,q = generate_prime(1000, 5000), generate_prime(1000, 5000) 
#generates 2 prime numbers P and Q

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

