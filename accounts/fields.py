from django.db import models
from .encryption import field_encryption

class EncryptedCharField(models.CharField):
    """
    A CharField that automatically encrypts and decrypts values.
    """
    
    def __init__(self, *args, **kwargs):
        # Remove max_length from kwargs if not provided, as it's required for CharField
        if 'max_length' not in kwargs:
            kwargs['max_length'] = 255
        super().__init__(*args, **kwargs)
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return field_encryption.decrypt(value)
    
    def to_python(self, value):
        if isinstance(value, str) or value is None:
            return value
        return field_encryption.decrypt(value)
    
    def get_prep_value(self, value):
        if value is None:
            return value
        return field_encryption.encrypt(value)

class EncryptedTextField(models.TextField):
    """
    A TextField that automatically encrypts and decrypts values.
    """
    
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return field_encryption.decrypt(value)
    
    def to_python(self, value):
        if isinstance(value, str) or value is None:
            return value
        return field_encryption.decrypt(value)
    
    def get_prep_value(self, value):
        if value is None:
            return value
        return field_encryption.encrypt(value)