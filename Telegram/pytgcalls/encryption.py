from cryptography.fernet import Fernet

class ConfigEncryption:
    def __init__(self, key: str):
        self.cipher_suite = Fernet(key)
    
    def encrypt(self, data: str) -> str:
        """Encrypt data"""
        return self.cipher_suite.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data"""
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()
