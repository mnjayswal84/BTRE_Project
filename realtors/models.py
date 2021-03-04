from django.db import models
from datetime import datetime
from django.contrib.auth.models import User 
class Realtor(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20, default=0)
    is_mvp = models.BooleanField(default=False)
    hire_date = models.DateTimeField(default=datetime.now, blank=True)
    
    def __str__(self):
        return self.user_id.first_name

    def get_realtor_name(self):
        return self.user_id.first_name

    def get_realtor_email(self):
        return self.user_id.email 