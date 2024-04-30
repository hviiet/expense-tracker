from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    profile_picture = models.CharField(max_length=100, blank=True, null=True)
    cookie = models.CharField(max_length=100, blank=True, null=True)

class IncomeType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ExpenseType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income_type = models.ForeignKey(IncomeType, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    amount = models.FloatField()
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

