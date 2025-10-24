from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class StrongPasswordValidator:
    """
    Validate that the password meets strong security requirements.
    """
    
    def __init__(self, min_length=12):
        self.min_length = min_length

    def validate(self, password, user=None):
        # Check minimum length
        if len(password) < self.min_length:
            raise ValidationError(
                _("Password must contain at least %(min_length)d characters."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )
        
        # Check for uppercase letter
        if not any(char.isupper() for char in password):
            raise ValidationError(
                _("Password must contain at least one uppercase letter."),
                code='password_no_upper',
            )
        
        # Check for lowercase letter
        if not any(char.islower() for char in password):
            raise ValidationError(
                _("Password must contain at least one lowercase letter."),
                code='password_no_lower',
            )
        
        # Check for digit
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                _("Password must contain at least one digit."),
                code='password_no_digit',
            )
        
        # Check for special character
        special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(char in special_characters for char in password):
            raise ValidationError(
                _("Password must contain at least one special character."),
                code='password_no_special',
            )
        
        # Check for common patterns (optional additional checks)
        common_patterns = ['123', 'abc', 'qwerty']
        for pattern in common_patterns:
            if pattern in password.lower():
                raise ValidationError(
                    _("Password must not contain common patterns like '123' or 'abc'."),
                    code='password_common_pattern',
                )
        
        return password

    def get_help_text(self):
        return _(
            "Your password must contain at least %(min_length)d characters, "
            "including uppercase letters, lowercase letters, digits, and special characters."
        ) % {'min_length': self.min_length}