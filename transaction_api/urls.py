from django.urls import path, include
from rest_framework.routers import DefaultRouter
from storage.views import TransactionViewSet
from storage.auth_views import RegisterView, LoginView, ProfileView

# Router for TransactionViewSet (auto-generates CRUD URLs)
router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    # Simple authentication endpoints
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    path('api/auth/login/', LoginView.as_view(), name='login'),
    path('api/auth/profile/', ProfileView.as_view(), name='profile'),
    
    # Transaction endpoints (via router)
    path('api/', include(router.urls)),
]