from django.contrib.auth.forms import UserCreationForm
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



