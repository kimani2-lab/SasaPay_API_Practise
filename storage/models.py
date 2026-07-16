from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    reference = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['reference']),
            models.Index(fields=['status']),
        ]
    
    def clean(self):
        """Validate model fields"""
        if self.amount <= 0:
            raise ValidationError({'amount': 'Amount must be greater than 0'})
        if self.status not in dict(self.STATUS_CHOICES):
            raise ValidationError({'status': f'Invalid status. Choose from: {[s[0] for s in self.STATUS_CHOICES]}'})
    
    def save(self, *args, **kwargs):
        """Run validation before saving"""
        self.clean()
        super().save(*args, **kwargs)
    
    def mark_completed(self):
        """Mark transaction as completed"""
        if self.status == 'completed':
            raise ValidationError('Transaction is already completed')
        self.status = 'completed'
        self.save()
    
    def mark_failed(self):
        """Mark transaction as failed"""
        if self.status in ['completed', 'cancelled']:
            raise ValidationError(f'Cannot mark completed or cancelled transaction as failed')
        self.status = 'failed'
        self.save()
    
    def __str__(self):
        return f"{self.reference} - {self.amount} ({self.status})"