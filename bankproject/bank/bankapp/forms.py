
from django import forms
from .models import Account, Transaction, User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class AccountCreationForm(forms.ModelForm):
    initial_deposit = forms.DecimalField(decimal_places=2, max_digits=10, required=True, initial=0.0, help_text="Enter the amount to deposit initially")

    class Meta:
        model = Account
        fields = ['account_number', 'account_type', 'initial_deposit']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount']
