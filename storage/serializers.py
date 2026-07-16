from rest_framework import serializers
from django.core.exceptions import ValidationError
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'reference', 'amount', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_amount(self, value):
        """Validate amount is positive"""
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        if value > 499999.99:
            raise serializers.ValidationError("Amount exceeds maximum limit")
        return value
    
    def validate_reference(self, value):
        """Validate reference format"""
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("Reference cannot be empty")
        if len(value) < 3:
            raise serializers.ValidationError("Reference must be at least 3 characters")
        return value.upper()
    
    def validate_status(self, value):
        """Validate status is a valid choice"""
        valid_statuses = [choice[0] for choice in Transaction.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(f"Invalid status. Choose from: {valid_statuses}")
        return value
    
    def create(self, validated_data):
        """Create transaction with error handling"""
        try:
            return Transaction.objects.create(**validated_data)
        except Exception as e:
            raise serializers.ValidationError(f"Error creating transaction: {str(e)}")