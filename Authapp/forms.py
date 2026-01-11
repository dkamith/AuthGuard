from django import forms 
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
User= get_user_model()

class SignupForm(forms.ModelForm):
    password1=forms.CharField(label="Password",widget=forms.PasswordInput)
    password2=forms.CharField(label="Confirm Password",widget=forms.PasswordInput)
     
    
    class Meta:
        model=User
        fields=["username"]

    def clean_username(self):
        username=self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exsist")
        else:
            return username
    def clean(self):
        cleaned_data= super().clean()
        if cleaned_data.get("password1")!=cleaned_data.get("password2"):
            raise ValidationError("password doesnot match")
        return cleaned_data
    