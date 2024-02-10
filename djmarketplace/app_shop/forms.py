import re
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import User, GoodCart
from django import forms

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'password1', 'password2')



class CartAddForm(forms.ModelForm):

    class Meta:
        model = GoodCart
        fields = ('good_num', )


class BalanceForm(forms.Form):
    card_number = forms.CharField(
        label='Номер карты',
        max_length=16,
        widget=forms.TextInput(attrs={'placeholder': '16 цифр без пробелов'})
    )
    expiry_date = forms.CharField(
        label='Дата окончания действия',
        max_length=4,
        widget=forms.TextInput(attrs={'placeholder': 'ММГГ'})
    )
    cvv = forms.CharField(
        label='CVV',
        max_length=3,
        widget=forms.TextInput(attrs={'placeholder': '123'})
    )
    amount = forms.FloatField(label='Сумма пополнения')

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        card_number = cleaned_data.get('card_number')
        expiry_date = cleaned_data.get('expiry_date')
        cvv = cleaned_data.get('cvv')

        if amount is not None and amount <= 0:
            raise ValidationError("Сумма пополнения должна быть больше нуля.")

        if card_number is not None and not re.match(r'^\d{16}$', card_number):
            raise ValidationError("Некорректный номер карты. Номер карты должен состоять из 16 цифр.")

        if expiry_date is not None and not re.match(r'^(0[1-9]|1[0-2])[0-9]{2}$', expiry_date):
            raise ValidationError("Некорректная дата окончания действия карты. Формат должен быть ММГГ.")

        if cvv is not None and not re.match(r'^\d{3}$', cvv):
            raise ValidationError("Некорректный CVV. CVV должен состоять из 3 цифр.")

        return cleaned_data
