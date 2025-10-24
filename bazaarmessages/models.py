from django.db import models
from accounts.models import User
from orders.models import Order
from accounts.fields import EncryptedTextField

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='messages', blank=True, null=True)
    content = EncryptedTextField()
    is_read = models.BooleanField(default=False)  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        # For display purposes, we'll show a generic message since content is encrypted
        return f"Message from {self.sender} to {self.receiver}"