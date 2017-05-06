from django.contrib.auth.models import User
from django.db import models
import PIL.Image as Image


class UserInfo(models.Model):
    userId = models.OneToOneField(User)
    image = models.ImageField(upload_to= 'photos', blank= True)
