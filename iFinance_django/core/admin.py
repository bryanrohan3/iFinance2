from django.contrib import admin
from core.models import *

# Register your models here.
admin.site.register(UserProfile)

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'password' ,'first_name', 'last_name')

admin.site.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'date')    

admin.site.register(Income)    
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'date')

admin.site.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'budget_name', 'budget_amount', 'start_date', 'end_date')