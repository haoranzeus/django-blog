from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='user name', max_length=100)
    password = forms.CharField()


class RegisterForm(forms.Form):
    username = forms.CharField(label='user name', max_length=100)
    password1 = forms.CharField()
    password2 = forms.CharField()


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=190)
