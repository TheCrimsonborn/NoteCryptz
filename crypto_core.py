import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag

# Constants
SALT_LEN = 16
IV_LEN = 12
ITERATIONS = 400_000 # Higher than C++ version to accommodate modern standards

class CryptoCore:
    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=ITERATIONS,
        )
        return kdf.derive(password.encode('utf-8'))

    @staticmethod
    def encrypt(plaintext_str: str, password: str) -> bytes:
        salt = os.urandom(SALT_LEN)
        iv = os.urandom(IV_LEN)
        
        key = CryptoCore._derive_key(password, salt)
        aesgcm = AESGCM(key)
        
        plaintext_bytes = plaintext_str.encode('utf-8')
        # The encrypt method appends the 16-byte authentication tag automatically
        ciphertext_with_tag = aesgcm.encrypt(iv, plaintext_bytes, None)
        
        # Format: [Salt][IV][Ciphertext + Tag]
        return salt + iv + ciphertext_with_tag

    @staticmethod
    def decrypt(ciphertext_data: bytes, password: str) -> str:
        if len(ciphertext_data) < SALT_LEN + IV_LEN + 16: # 16 is tag length
            raise ValueError("Invalid file format: Data too short.")
        
        salt = ciphertext_data[:SALT_LEN]
        iv = ciphertext_data[SALT_LEN:SALT_LEN+IV_LEN]
        ciphertext_with_tag = ciphertext_data[SALT_LEN+IV_LEN:]
        
        key = CryptoCore._derive_key(password, salt)
        aesgcm = AESGCM(key)
        
        try:
            plaintext_bytes = aesgcm.decrypt(iv, ciphertext_with_tag, None)
            return plaintext_bytes.decode('utf-8')
        except InvalidTag:
            raise ValueError("Decryption failed. Incorrect password or corrupted data.")
