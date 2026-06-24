from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Transaction, Category


class SignUpForm(UserCreationForm):
    """Simple sign-up form using Django's built-in User model."""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Tailwind classes to every field for consistent styling
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full rounded-lg border border-gray-300 dark:border-gray-600 '
                         'bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 '
                         'px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500'
            })


class TransactionForm(forms.ModelForm):
    """Form to add or edit an income/expense transaction."""

    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'transaction_type', 'category', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Only show categories belonging to the logged-in user
        if user is not None:
            self.fields['category'].queryset = Category.objects.filter(user=user)

        base_classes = (
            'w-full rounded-lg border border-gray-300 dark:border-gray-600 '
            'bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 '
            'px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500'
        )
        for field in self.fields.values():
            field.widget.attrs.update({'class': base_classes})


class CategoryForm(forms.ModelForm):
    """Form to add a new category."""

    class Meta:
        model = Category
        fields = ['name', 'category_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_classes = (
            'w-full rounded-lg border border-gray-300 dark:border-gray-600 '
            'bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 '
            'px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500'
        )
        for field in self.fields.values():
            field.widget.attrs.update({'class': base_classes})
