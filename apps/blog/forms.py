from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label='user name', max_length=100)
    # email = forms.EmailField(label='email')
    password = forms.CharField()


class RegisterForm(forms.Form):
    username = forms.CharField(label='user name', max_length=100)
    email = forms.EmailField(label='email')
    password1 = forms.CharField()
    password2 = forms.CharField()


class CommentForm(forms.Form):
    comment = forms.CharField(max_length=190)
