import rsa_module

keys = rsa_module.keygen()
e = keys[0]
n = keys[1]
d = keys[2]

message = "nic1"

enc = rsa_module.encrypt((e,n), message)
print(enc)

dec = rsa_module.decrypt(d, (e,n), enc)
print(dec)