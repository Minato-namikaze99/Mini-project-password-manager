import random 
import math
import pandas as pd
 
# Counter to keep track of key operations
key_operations = {
    'Number of digits':[],
    'Key Size': [],
    'Total Key Operations': []
}

def is_prime(n, k=5):
    """Rabin-Miller primality test."""
    count=0
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
	count +=1
        a = random.randint(2, n - 1)
        x = (a**d)%n
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
	    count +=1
            x = (x**2)%n
            if x == n - 1:
                break
        else:
            return False
    return True, count

def generate_prime(min_value, max_value): 
    prime_generation_count = 0
    while True:
        prime_generation_count += 1
        prime = random.randint(min_value, max_value)
	pp, count = is_prime(prime)
        if pp:
            return prime, prime_generation_count+count

def mod_inverse(e, phi):
    mod_inverse_count = 0
    for d in range(3, phi):
        mod_inverse_count += 1
        if (d * e) % phi == 1:
            return d, mod_inverse_count
    
    raise ValueError("Mod_Inverse does not exist")

def run_rsa(min_value, max_value):
    p, prime_generation_count_p = generate_prime(min_value, max_value)
    q, prime_generation_count_q = generate_prime(min_value, max_value)
    
    while p == q: 
        q, prime_generation_count_q = generate_prime(min_value, max_value)

    n = p * q 

    phi_n = (p - 1) * (q - 1)

    e = random.randint(3, phi_n) 

    total_key_operations = prime_generation_count_p + prime_generation_count_q
    
    coprime_check_count = 0
    while math.gcd(e, phi_n) != 1: 
        e = random.randint(3, phi_n) 
        coprime_check_count += 1
        total_key_operations += 1

    d, mod_inverse_count = mod_inverse(e, phi_n)
    total_key_operations += mod_inverse_count

    key_operations['Key Size'].append(math.ceil(math.log2(max(p, q))))
    key_operations['Total Key Operations'].append(total_key_operations)

l1 = [[0,9],[10,99],[100,999],[1000, 9999],[10000, 99999],[100000, 999999]]
c99 = 0
for i in l1:
    run_rsa(i[0], i[1])
    c99+=1
    key_operations['Number of digits'].append(c99)
    print(c99)
df = pd.DataFrame(key_operations)
print(df)

import matplotlib.pyplot as plt

# Assuming df is your DataFrame containing the data
plt.figure(figsize=(8, 6))
plt.scatter(df['Key Size'], df['Total Key Operations'], color='blue')
plt.title('RSA Key Operations vs Key Size')
plt.xlabel('Key Size (bits)')
plt.ylabel('Total Key Operations')
plt.grid(True)

# Save the plot as an image
plt.savefig('rsa_key_operations_plot_new.png')

# Show the plot
plt.show()
