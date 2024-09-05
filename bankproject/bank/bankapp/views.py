
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, AccountCreationForm, TransactionForm
from .models import Account, Transaction
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'account/login.html')

@login_required
def dashboard(request):
    try:
        account = Account.objects.get(user=request.user)
    except Account.DoesNotExist:
        return redirect('create-account')  # Redirect to account creation if no account found

    transactions = Transaction.objects.filter(account=account).order_by('-date')
    return render(request, 'account/dashboard.html', {
        'account': account,
        'transactions': transactions,
    })

@login_required
def create_account(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            initial_deposit = form.cleaned_data['initial_deposit']
            account.balance = initial_deposit  # Set the initial balance
            account.save()
            return redirect('dashboard')  # Redirect to dashboard after account creation
    else:
        form = AccountCreationForm()
    return render(request, 'account/create-account.html', {'form': form})

@login_required
def transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = Account.objects.get(user=request.user)
            if transaction.transaction_type == 'Withdrawal' and transaction.amount > transaction.account.balance:
                return render(request, 'account/transaction.html', {'form': form, 'error': 'Insufficient balance'})
            else:
                if transaction.transaction_type == 'Withdrawal':
                    transaction.account.balance -= transaction.amount
                else:
                    transaction.account.balance += transaction.amount
                transaction.account.save()
                transaction.save()
                return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'account/transaction.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
