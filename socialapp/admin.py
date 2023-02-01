from django.contrib import admin
from django.contrib.auth.models import User, Group
from models import Profile

# Un registering the groups as it is not required in the social web application
admin.site.unregister(Group)


# Register your models here.
class UserAdmin(admin.ModelAdmin):

    model = User

    # Only display the "username" field

    fields = ["username"]
    

#Un registering the existing user model from the admin panel
admin.site.unregister(User)

# Registered the user model again passing the custom admin class just created.
admin.site.register(User, UserAdmin)

#Registering the profile model created for users
admin.site.register(Profile)