from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class UserSignupForm(forms.ModelForm):

    """
    Form to register a new user in the data base    
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'signup-form'
        # Dictionary to add the extra attributes to the crispy form
        self.helper.attrs = {
            # Redirecting on the save to signup page again
            'hx-post': reverse_lazy('signup'),
            # To replace the form with the information returned by django
            'hx-target': '#signup-form',
            # Ajax swap to replace the outer HTML (Avoiding placing html inside the target - form inside form)
            'hx-swap': 'outerHTML'
        }
        self.helper.add_input(Submit('submit', 'Submit'))

    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


    """
    Function to validate username before saving to database    
    """
    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) <= 3:
            raise forms.ValidationError("Username is too short")
        return username

      
    """
    Function to hash password before saving to database    
    """
   
    def save(self, commit=True):
        """ Hash user's password on save """
        user = super().save(commit=False)
        # resetting the password to insert the hash version of password
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return 

# class UserLoginForm(forms.Form):
#     pass