from django.db import models

class SellerProfile(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='seller_profile')
    store_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.store_name} ({self.user.username})"