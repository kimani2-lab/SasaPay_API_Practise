from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionViewSet(ModelViewSet):
    """A simple transaction viewset with standard CRUD operations."""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    # Create: POST /api/transactions/
    # def get (self, transaction): 
    # Retrieve: GET /api/transactions/{id}/
    # Update: PUT /api/transactions/{id}/
    # Partial Update: PATCH /api/transactions/{id}/
    # Delete: DELETE /api/transactions/{id}/
