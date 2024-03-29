from django import forms
from .models import Profile, Post
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth import authenticate
import datetime


class UserSignupForm(forms.ModelForm):
    """
    - Form to register a new user in the data base
    - HTMX for dynamic navigation from login to user home page without loading page
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "signup-form"
        # Dictionary to add the extra attributes to the crispy form
        self.helper.attrs = {
            # Redirecting on the save to signup page again
            "hx-post": reverse_lazy("signup"),
            # To replace/swap the form with the information returned by django
            "hx-target": "#signup-form",
            # Ajax swap to replace the outer HTML (Avoiding placing html inside the target - form inside form)
            "hx-swap": "innerHTML",
        }
        self.helper.add_input(
            Submit(
                "submit",
                "Submit",
                # Tailwind CSS class reference for button
                css_class="bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded",
            )
        )

    # Two password fields created to match it with each other before pushing to backend
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "off", "placeholder": "Enter the password"}
        ),
    )

    password2 = forms.CharField(
        label="Repeat Password",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "autocomplete": "off", "placeholder": "Enter the password"}
        ),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password1", "password2"]

    """
    Function to validate username before saving to database    
    """

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) <= 3:
            raise forms.ValidationError("Username is too short")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords does not match")
        return password2

    """
    Function to hash password before saving to database    
    """

    def save(self, commit=True):
        """Hash user's password on save"""
        user = super().save(commit=False)
        # resetting the password to insert the hash version of password
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return


class UserLoginForm(forms.Form):
    """
    - Form to login into the social web application.
    - Errors are identified using the form "Validation Error" class.
    - HTMX for dynamic navigation from login to user home page without loading page
    """

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput(attrs={"autocomplete": "off"}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise forms.ValidationError("Invalid username or password")

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserProfileForm(forms.ModelForm):
    """
    - Form to login show user profile.
    - Errors are identified using the form "Validation Error" class.
    """

    birthdate = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
    image = forms.ImageField()

    """
    Function to validate birth date is on/before today date    
    """

    def clean_birthdate(self):
        birthdate = self.cleaned_data["birthdate"]
        if birthdate >= datetime.date.today():
            raise forms.ValidationError("Please enter date before today's date")
        return birthdate

    class Meta:
        model = Profile
        fields = ["country", "birthdate", "image"]


class PostForm(forms.ModelForm):
    """
    - Form for submitting the post
    - Validation provided to accept only images as input.
    - HTMX for dynamic web after submitting the post
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = "post-form"
        # Dictionary to add the extra attributes to the crispy form
        self.helper.attrs = {
            # Redirecting on the save to signup page again
            "hx-post": reverse_lazy("home"),
            # To replace/swap the form with the information returned by django
            "hx-target": "#post-form",
            # Ajax swap to replace the outer HTML (Avoiding placing html inside the target - form inside form)
            "hx-swap": "outerHTML",
        }

    text = forms.CharField(max_length=140, widget=forms.Textarea(attrs={"rows": 3}))
    image = forms.ImageField(
        required=False,
        error_messages={"invalid": "Image files only"},
        widget=forms.FileInput,
    )

    class Meta:
        model = Post
        fields = ["text", "image"]
