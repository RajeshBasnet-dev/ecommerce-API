from cryptography.fernet import Fernet
from django.conf import settings
import base64
import os

class FieldEncryption:
    """
    Utility class for encrypting and decrypting sensitive data.
    """
    
    def __init__(self):
        # Get encryption key from environment variable or generate one
        encryption_key = getattr(settings, 'FIELD_ENCRYPTION_KEY', None)
        if encryption_key:
            # Ensure the key is properly formatted for Fernet
            if isinstance(encryption_key, str):
                encryption_key = encryption_key.encode()
            # Pad or truncate to 32 bytes if needed
            if len(encryption_key) < 32:
                encryption_key = encryption_key.ljust(32, b'\0')
            elif len(encryption_key) > 32:
                encryption_key = encryption_key[:32]
            # Base64 encode for Fernet
            self.key = base64.urlsafe_b64encode(encryption_key)
        else:
            # Generate a key if none is provided (not recommended for production)
            self.key = Fernet.generate_key()
        
        self.cipher_suite = Fernet(self.key)
    
    def encrypt(self, value):
        """
        Encrypt a value.
        """
        if value is None:
            return None
        if isinstance(value, str):
            value = value.encode('utf-8')
        encrypted_value = self.cipher_suite.encrypt(value)
        return encrypted_value.decode('utf-8')
    
    def decrypt(self, encrypted_value):
        """
        Decrypt a value.
        """
        if encrypted_value is None:
            return None
        encrypted_bytes = encrypted_value.encode('utf-8')
        decrypted_bytes = self.cipher_suite.decrypt(encrypted_bytes)
        return decrypted_bytes.decode('utf-8')

# Global instance
field_encryption = FieldEncryption()