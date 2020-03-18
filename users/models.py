from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver

class CustomUser(AbstractUser):
    """
    Custom User model that will be used in authentication process, instead of default Django User model
    """

    # Set is_staff as True, because we want every registered user to be able to login to admin page
    is_staff = models.BooleanField(default=True, help_text='Designates whether the user can log into this admin site.',
                                   verbose_name='staff status')

    def __str__(self):
        return self.email


class LogEntry(models.Model):
    """
    Model for logging user login, logout, and failed login
    """

    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True, verbose_name='IP')
    email = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.email, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.email, self.ip)

    class Meta:
        ordering = ('-id',)
        verbose_name_plural = 'Log Entries'
        verbose_name = 'Log Entry'


@receiver(post_save, sender=CustomUser)
def add_default_permission(sender, instance, **kwargs):
    """
    Give default permission 'Can change profile' to saved CustomUser object
    :param sender: CustomUser Class
    :param instance: CustomUser object that is being saved
    """
    if instance.is_superuser == False:
        can_change_profile = Permission.objects.get(name='Can change profile')
        instance.user_permissions.add(can_change_profile)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    """
    Called everytime user performed login successfully.
    LogEntry objects will be created, with 'user_logged_in' as action
    """
    ip = request.META.get('REMOTE_ADDR')
    LogEntry.objects.create(action='user_logged_in', ip=ip, email=user.email)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    """
    Called everytime user performed logout successfully.
    LogEntry objects will be created, with 'user_logged_out' as action
    """
    ip = request.META.get('REMOTE_ADDR')
    LogEntry.objects.create(action='user_logged_out', ip=ip, email=user.email)


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
    """
    Called everytime user failed to login.
    LogEntry objects will be created, with 'user_login_failed' as action
    """
    ip = request.META.get('REMOTE_ADDR')
    LogEntry.objects.create(action='user_login_failed', ip=ip, email=credentials.get('email', None))