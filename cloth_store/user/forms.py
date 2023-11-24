from.models import User
from django import forms


from django.contrib.auth.forms import PasswordChangeForm

class ChangePasswordForm(forms.Form):
    # old_password = forms.CharField(
    #     widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}),
    #     label='',
    # )
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label='',
    )


class ProductSearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search...'}))