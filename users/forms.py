from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    """
    Form that will be used to create the user in CustomUserAdmin
    """

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username',)

class CustomUserChangeForm(UserChangeForm):
    """
    Form that will be used to change the user in CustomUserAdmin
    """

    class Meta:
        model = CustomUser
        fields = ('email', 'username',)


class RegistrationForm(UserCreationForm):
    """
    Form that will be used in signup process
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name')