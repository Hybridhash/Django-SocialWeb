from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django_countries.fields import CountryField
from datetime import date
from django.core.validators import MaxValueValidator

# class AppUser(models.Model):
# user = models.OneToOneField(User, on_delete=models.CASCADE)
# contact = models.CharField(max_length=13, null=True, blank=True)

# def __unicode__(self):
#     return self.user.username


# Create your models here.
class Profile(models.Model):

    # There is one to one relationship between profile and user
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(blank_label="(select country)")
    birthdate = models.DateField(
        null=False, blank=False, validators=[MaxValueValidator(limit_value=date.today)]
    )
    image = models.ImageField(
        upload_to="images/", null=True, default="images/undraw_cabin.jpg"
    )
    # It allows to follow someone only without following back
    friends = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False, blank=True
    )

    def __str__(self):
        return str(self.user.username)
