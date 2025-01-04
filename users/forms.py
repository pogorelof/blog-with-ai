from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model


input_class = 'bg-gray-100 outline-none rounded w-full p-1'

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': input_class}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': input_class}))

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': input_class}))
    email = forms.EmailField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': input_class}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': input_class}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': input_class}))
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2', 'photo']
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Указанный email уже существует')
        return email