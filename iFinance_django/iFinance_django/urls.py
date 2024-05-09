from django.contrib import admin
from django.urls import path, include
from core import viewsets
from rest_framework import routers

api_router = routers.DefaultRouter()
api_router.register(r'test', viewsets.TestViewSet)
api_router.register(r'user', viewsets.UserViewSet)
api_router.register(r'expense', viewsets.ExpenseViewSet)
api_router.register(r'income', viewsets.IncomeViewSet)
api_router.register(r'budget', viewsets.BudgetViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('auth/login/', viewsets.CustomAuthentication.as_view()),
    path('api/', include(api_router.urls)),
    path('api/bank_balance/', viewsets.UserViewSet.get_bank_balance, name='get_bank_balance'),
]