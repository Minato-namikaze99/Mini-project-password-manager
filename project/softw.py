import os

# Define your encryption function here
def encrypt(text, public_key):
    # Your encryption algorithm goes here
    # Use the provided public key for encryption
    encrypted_text = text + " [Encrypted with key: {}]".format(public_key)
    return encrypted_text

# Define your decryption function here
def decrypt(text):
    # Your decryption algorithm goes here
    # Extract and validate the public key from the encrypted text
    # Decrypt the text using the corresponding private key
    decrypted_text = text.split("[Encrypted with key: ")[0]
    return decrypted_text

# Function to encrypt a file
def encrypt_file(file_path, public_key):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        encrypted_content = encrypt(content, public_key)
        
        with open(file_path, 'w') as file:
            file.write(encrypted_content)
        
        print("File encrypted successfully!")
    except Exception as e:
        print("Error:", e)

# Function to decrypt a file
def decrypt_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        
        decrypted_content = decrypt(content)
        
        with open(file_path, 'w') as file:
            file.write(decrypted_content)
        
        print("File decrypted successfully!")
    except Exception as e:
        print("Error:", e)

# Main function
def main():
    file_path = input("Enter the path of the text file: ")
    if os.path.exists(file_path):
        operation = input("Enter 'E' to encrypt or 'D' to decrypt: ")
        if operation.upper() == 'E':
            public_key = input("Enter the public key: ")
            encrypt_file(file_path, public_key)
        elif operation.upper() == 'D':
            decrypt_file(file_path)
        else:
            print("Invalid operation.")
    else:
        print("File not found.")

if __name__ == "__main__":
    main()
