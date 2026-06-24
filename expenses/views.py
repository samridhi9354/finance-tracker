from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from django.urls import reverse_lazy

from .models import Transaction, Category
from .forms import TransactionForm, CategoryForm, SignUpForm


# ---------------------------
# Authentication Views
# ---------------------------

class CustomLoginView(LoginView):
    """Custom login view that uses our styled template."""
    template_name = 'expenses/login.html'


def signup_view(request):
    """Handle new user registration."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            # Create some default categories for the new user
            default_categories = [
                ('Salary', Category.INCOME),
                ('Freelance', Category.INCOME),
                ('Food', Category.EXPENSE),
                ('Rent', Category.EXPENSE),
                ('Travel', Category.EXPENSE),
                ('Shopping', Category.EXPENSE),
                ('Bills', Category.EXPENSE),
            ]
            for name, c_type in default_categories:
                Category.objects.get_or_create(user=user, name=name, category_type=c_type)

            messages.success(request, 'Account created successfully! Welcome aboard.')
            return redirect('dashboard')
    else:
        form = SignUpForm()

    return render(request, 'expenses/signup.html', {'form': form})


# ---------------------------
# Dashboard
# ---------------------------

@login_required
def dashboard(request):
    """
    Main dashboard showing:
    - total income, total expense, current balance
    - recent transactions
    - a simple category-wise breakdown for charts
    """
    transactions = Transaction.objects.filter(user=request.user)

    total_income = transactions.filter(transaction_type=Transaction.INCOME).aggregate(
        total=Sum('amount'))['total'] or 0
    total_expense = transactions.filter(transaction_type=Transaction.EXPENSE).aggregate(
        total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    recent_transactions = transactions[:5]

    # Category-wise expense breakdown (for the chart)
    category_data = (
        transactions.filter(transaction_type=Transaction.EXPENSE, category__isnull=False)
        .values('category__name')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )

    chart_labels = [item['category__name'] for item in category_data]
    chart_values = [float(item['total']) for item in category_data]

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'recent_transactions': recent_transactions,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
        'today': timezone.now().date(),
    }
    return render(request, 'expenses/dashboard.html', context)


# ---------------------------
# Transactions: list, add, edit, delete
# ---------------------------

@login_required
def transaction_list(request):
    """
    Show all transactions for the logged-in user, with optional
    filtering by type (income/expense) and search by title.
    """
    transactions = Transaction.objects.filter(user=request.user)

    transaction_type = request.GET.get('type')
    search_query = request.GET.get('q')

    if transaction_type in ['income', 'expense']:
        transactions = transactions.filter(transaction_type=transaction_type)

    if search_query:
        transactions = transactions.filter(
            Q(title__icontains=search_query) | Q(notes__icontains=search_query)
        )

    context = {
        'transactions': transactions,
        'transaction_type': transaction_type,
        'search_query': search_query or '',
    }
    return render(request, 'expenses/transaction_list.html', context)


@login_required
def add_transaction(request):
    """Add a new income or expense transaction."""
    if request.method == 'POST':
        form = TransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            messages.success(request, 'Transaction added successfully!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(user=request.user, initial={'date': timezone.now().date()})

    return render(request, 'expenses/transaction_form.html', {
        'form': form,
        'title': 'Add Transaction',
    })


@login_required
def edit_transaction(request, pk):
    """Edit an existing transaction (only if it belongs to the logged-in user)."""
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transaction updated successfully!')
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction, user=request.user)

    return render(request, 'expenses/transaction_form.html', {
        'form': form,
        'title': 'Edit Transaction',
    })


@login_required
def delete_transaction(request, pk):
    """Delete a transaction after confirmation."""
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        transaction.delete()
        messages.success(request, 'Transaction deleted.')
        return redirect('transaction_list')

    return render(request, 'expenses/transaction_confirm_delete.html', {'transaction': transaction})


# ---------------------------
# Categories: list, add, delete
# ---------------------------

@login_required
def category_list(request):
    """Show all categories for the logged-in user, and a form to add new ones."""
    categories = Category.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()

    return render(request, 'expenses/category_list.html', {
        'categories': categories,
        'form': form,
    })


@login_required
def delete_category(request, pk):
    """Delete a category (transactions using it will have category set to null)."""
    category = get_object_or_404(Category, pk=pk, user=request.user)

    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('category_list')

    return render(request, 'expenses/category_confirm_delete.html', {'category': category})
