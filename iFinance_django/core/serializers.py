from rest_framework import serializers
from core.models import test, UserProfile, Expense, Income, Budget
from django.contrib.auth.models import User
from django.db.models import Sum, F

class ABCSerializer(serializers.ModelSerializer):
    class Meta:
        model = test
        fields = '__all__'

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'email', 'password', 'first_name', 'last_name', 'bank_balance')

    def create(self, validated_data):
        user = User.objects.create_user( validated_data["email"], validated_data["email"], validated_data["password"])
        validated_data["user"] = user
        return UserProfile.objects.create(**validated_data)
        # return super().create(validated_data)
    

class UserPublicDetailsSerializer(serializers.ModelSerializer):
    user_object_id = serializers.IntegerField(source="user.id")
    class Meta:
        model = UserProfile
        fields = ('user_object_id','id', 'first_name', 'last_name', 'bank_balance')

    
class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Expense
        fields = ['id', 'user', 'category', 'category_name', 'amount', 'date', 'date_time_created']
        extra_kwargs = {
            'user': {
                'read_only': True,
            }
        }

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data["user"] = request.user

        # Deduct the expense amount from the budget amount
        budget_id = validated_data.get('budget')
        if budget_id:
            budget = Budget.objects.get(pk=budget_id)
            budget.budget_amount -= validated_data['amount']
            budget.save()

        return Expense.objects.create(**validated_data)

    


class IncomeSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Income
        fields = ['id', 'user', 'category', 'category_name', 'amount', 'date', 'date_time_created']
        extra_kwargs = {
            'user': {
                'read_only': True,
            }
        }

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data["user"] = request.user

        # Add the income amount to the user's bank balance
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.bank_balance += validated_data['amount']
        user_profile.save()

        # Create the income object
        return Income.objects.create(**validated_data)

    
class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = ['id', 'user', 'budget_name', 'budget_amount', 'start_date', 'end_date']
        extra_kwargs = {
            'user': {
                'read_only': True,
            }
        }

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data["user"] = request.user

         # Deduct the budget amount from the user's bank balance
        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.bank_balance -= validated_data['budget_amount']
        user_profile.save()

        return Budget.objects.create(**validated_data)
    
    # git commit

