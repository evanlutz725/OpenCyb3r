from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# -------------------------
# Caesar Functions
# -------------------------
def caesar_encrypt(text: str, shift: int) -> str:
    """Encrypt text using a Caesar cipher with the given shift."""
    result = []
    for char in text:
        if char.isupper():
            shifted = chr((ord(char) - 65 + shift) % 26 + 65)
            result.append(shifted)
        elif char.islower():
            shifted = chr((ord(char) - 97 + shift) % 26 + 97)
            result.append(shifted)
        else:
            result.append(char)
    return ''.join(result)

def caesar_decrypt(text: str, shift: int) -> str:
    """Decrypt text using a Caesar cipher with the given shift."""
    return caesar_encrypt(text, -shift)

# -------------------------
# XOR Functions
# -------------------------
def xor_encrypt(text: str, key: str) -> str:
    """
    Encrypt text using XOR encryption.
    Returns the result as a hexadecimal string.
    """
    text_bytes = text.encode('utf-8')
    key_bytes = key.encode('utf-8')
    cipher_bytes = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(text_bytes)])
    return cipher_bytes.hex()

def xor_decrypt(cipher_hex: str, key: str) -> str:
    """
    Decrypt text that was encrypted using XOR encryption.
    Assumes input is a hexadecimal string.
    """
    cipher_bytes = bytes.fromhex(cipher_hex)
    key_bytes = key.encode('utf-8')
    plain_bytes = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(cipher_bytes)])
    return plain_bytes.decode('utf-8')

# -------------------------
# AES-128 Functions
# -------------------------
def aes_encrypt(plaintext: str, key: str) -> str:
    """
    Encrypt plaintext using AES-128 in CBC mode.
    The key is normalized to 16 bytes (AES-128).
    Returns a hex-encoded string that includes the IV followed by the ciphertext.
    """
    key_bytes = key.encode('utf-8')
    # Ensure key is 16 bytes long (pad with null bytes or trim)
    if len(key_bytes) < 16:
        key_bytes = key_bytes.ljust(16, b'\0')
    elif len(key_bytes) > 16:
        key_bytes = key_bytes[:16]
    iv = get_random_bytes(16)
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    padded_text = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_text)
    # Prepend the IV for use in decryption
    return (iv + ciphertext).hex()

def aes_decrypt(cipher_hex: str, key: str) -> str:
    """
    Decrypt ciphertext that was encrypted using AES-128 in CBC mode.
    Expects the input as a hex-encoded string with the IV prepended.
    """
    data = bytes.fromhex(cipher_hex)
    iv = data[:16]
    ciphertext = data[16:]
    key_bytes = key.encode('utf-8')
    if len(key_bytes) < 16:
        key_bytes = key_bytes.ljust(16, b'\0')
    elif len(key_bytes) > 16:
        key_bytes = key_bytes[:16]
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size)
    return plaintext.decode('utf-8')

# -------------------------
# Command-Line Interface
# -------------------------
def main():
    print("Encryption Tool: Caesar, XOR, AES-128")
    print("-------------------------------------------")
    
    # Step 1: Choose algorithm
    while True:
        algorithm = input("Choose algorithm number (caesar, xor, aes): ").strip().lower()
        if algorithm in ['caesar', 'xor', 'aes']:
            break
        print("Invalid algorithm. Please choose from: caesar, xor, aes.")
    
    # Step 2: Choose mode
    while True:
        mode = input("Choose mode (encrypt or decrypt): ").strip().lower()
        if mode in ['encrypt', 'decrypt']:
            break
        print("Invalid mode. Please choose 'encrypt' or 'decrypt'.")
    
    # Step 3: Enter text
    text = input("Enter the text: ")
    
    # Step 4: Get algorithm-specific parameters
    if algorithm == "caesar":
        while True:
            try:
                shift = int(input("Enter shift value (integer): "))
                break
            except ValueError:
                print("Invalid input. Please enter an integer for shift.")
    elif algorithm in ["xor", "aes"]:
        key = input(f"Enter key for {algorithm.upper()}: ")
    
    # Process the encryption/decryption
    result = None
    if algorithm == "caesar":
        if mode == "encrypt":
            result = caesar_encrypt(text, shift)
        else:  # mode == "decrypt"
            result = caesar_decrypt(text, shift)
    elif algorithm == "xor":
        if mode == "encrypt":
            result = xor_encrypt(text, key)
        else:  # mode == "decrypt"
            result = xor_decrypt(text, key)
    elif algorithm == "aes":
        if mode == "encrypt":
            result = aes_encrypt(text, key)
        else:  # mode == "decrypt"
            result = aes_decrypt(text, key)
    
    # Display result
    print("\nResult:")
    print(result)

if __name__ == "__main__":
    main()
