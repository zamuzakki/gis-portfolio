from django.contrib.gis.db import models as gis
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from users.models import CustomUser
import os

class BaseModel(models.Model):
    """
    Abstract Model to be inherited by other model in profile
    """

    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    class Meta:
        abstract = True

def user_photo_directory(instance, filename):
    """
    Callback for Profile photo upload
    :param instance: saved object (Profile)
    :param filename: uploaded photo_name
    :return: path of uploaded file
    """
    filename, ext = os.path.splitext(filename)
    return '{}/photo{}'.format(instance.user.username, ext)

class Expertise(BaseModel):
    """
    Model for available expertise, e.g Python, Django, HTML
    """
    name = models.CharField(max_length=15, blank=False, null=False)

    def __unicode__(self):
        return '{}'.format(self.name)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('name',)

class Profile(BaseModel):
    """
    Model for User Profile, has OnetoOne relationship with CustomUser
    """

    user = models.OneToOneField(CustomUser, null=False, default=1, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_photo_directory, null=True, blank=True)
    first_name = models.CharField(max_length=20, null=False, blank=False, default='')
    last_name = models.CharField(max_length=20, null=False, blank=False, default='')
    address = models.CharField(max_length=100, default='', null=False, blank=True)
    phone = PhoneNumberField(max_length=15, null=False, blank=True, default='')
    expertise = models.ManyToManyField(Expertise)
    location = gis.PointField(null=True, default=None, blank=True)

    def __unicode__(self):
        return '{} - {} - {}'.format(self.user.username, self.user.first_name + ' ' + self.user.last_name, self.phone)

    def __str__(self):
        return self.__unicode__()

    class Meta:
        ordering = ('-id',)

@receiver(post_save, sender=Profile)
def update_user_name(sender, instance, **kwargs):
    """
    Change User first_name and last_name when updating Profile
    first_name and last_name
    :param sender: Profile
    :param instance: Profile instance (saved Profile object)
    """
    if not instance.first_name == '':
        instance.user.first_name = instance.first_name
    if not instance.last_name == '':
        instance.user.last_name = instance.last_name
    instance.user.save()