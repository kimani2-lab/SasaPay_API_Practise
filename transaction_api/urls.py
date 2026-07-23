from django.urls import path, include
from rest_framework.routers import DefaultRouter
from storage.views import TransactionViewSet
from storage.auth_views import CustomTokenObtainPairView, TokenRefreshView, RegisterView

# Router for TransactionViewSet (auto-generates CRUD URLs)
router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    # JWT Authentication endpoints
    path('api/auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/login/token', CustomTokenObtainPairView.as_view(), name='login_token'),
    
    # User registration, login and profile
    path('api/auth/register/', RegisterView.as_view(), name='register'),
    # path('api/auth/profile/', ProfileView.as_view(), name='profile'),
   # path('api/auth/login/', loginView.as_view(), name='login_view'),

    # Transaction endpoints (via router)
    path('api/', include(router.urls)),
]