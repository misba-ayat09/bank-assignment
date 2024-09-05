from django.contrib.auth.models import User
from django.db import models

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    account_type = models.CharField(max_length=10, choices=[('Savings', 'Savings'), ('Current', 'Current')])
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.account_number}'

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=30, unique=True)
    transaction_type = models.CharField(max_length=10, choices=[('Deposit', 'Deposit'), ('Withdrawal', 'Withdrawal')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.transaction_type} - {self.amount}'
