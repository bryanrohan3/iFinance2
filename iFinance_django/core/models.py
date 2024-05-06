from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class test(models.Model):
    name = models.CharField(max_length=100)

# get user email/password
class UserProfile(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=100)

    # first and last name
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # bank balance to .2 decimals
    bank_balance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0.00)

    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)

# Expense Form
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_choices = [
        ('0', 'Food'),
        ('1', 'Transport'),
        ('2', 'Utilities'),
        ('3', 'Entertainment'),
        ('4', 'Other'),
    ]
    category = models.CharField(max_length=100, choices=category_choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    date_time_created = models.DateTimeField(auto_now_add=True)

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_choices = [
        ('0', 'Salary'),
        ('1', 'Bonus'),
        ('2', 'Gift'),
        ('3', 'Other'),
    ]
    category = models.CharField(max_length=100, choices=category_choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    date_time_created = models.DateTimeField(auto_now_add=True)


# budget 
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget_name = models.CharField(max_length=100)
    budget_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()




# bill
# profile
# bank balance
# categories

# model as catergory and create multiple objects
