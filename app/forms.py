from django import forms


class SignupForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'text'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'text'}))
    house = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'number'}))
    line1 = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'text'}))
    postcode = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'text'}))
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'tel'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'email'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}))
    password_confirm = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}))


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'email'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'password'}))
