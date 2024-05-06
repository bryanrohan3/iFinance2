from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import viewsets, mixins, status
from .models import test, UserProfile, Expense, Income, Budget
from .serializers import ABCSerializer, UserSerializer, UserPublicDetailsSerializer, ExpenseSerializer, IncomeSerializer, BudgetSerializer
from rest_framework.decorators import action
from django.contrib.auth import authenticate, login
from django.http import JsonResponse


class CustomAuthentication(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response(
                {'error': 'We couldn\'t log you in with those credentials.'})
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
        })

class TestViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = test.objects.all() 
    serializer_class = ABCSerializer

    @action(detail=False, methods=['GET'])
    def refresh(self, request):
        print(request.user.first_name)
        return Response(
            {},
            status=status.HTTP_200_OK,)

class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['POST'], permission_classes=[])
    def login(self, request):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        user = authenticate(username=email, password=password)
        if user is not None:
            profile = UserProfile.objects.get(user=user)
            serializer = UserPublicDetailsSerializer(profile)
            token, created = Token.objects.get_or_create(user=user)
            # return Response(serializer.data)
            login(request, user)
            print(token)
            return JsonResponse({'message': 'Login successful', 'user': serializer.data, 'token': token.key})
        else:
            return JsonResponse({'error': 'Invalid email or password'}, status=400)
        

    @action(detail=False, methods=['GET'])
    def get_current_user_details(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserPublicDetailsSerializer(profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['GET'])
    def get_bank_balance(self, request):
        profile = UserProfile.objects.get(user=request.user)
        return Response(profile.bank_balance)

class ExpenseViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
    ):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        request = self.request
        user = request.user
        return queryset.filter(user=user)

class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
