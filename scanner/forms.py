from django import forms

class qrcontent(forms.Form):
  qrtext = forms.CharField(max_length=300,required=True,label="Qr text" ,widget=forms.TextInput(attrs={'readonly':'readonly'}))
  registrar = forms.CharField(max_length=300,required=True, label="Registration By:",widget=forms.TextInput(attrs={'readonly':'readonly'}))