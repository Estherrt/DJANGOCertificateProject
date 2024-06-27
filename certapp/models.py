from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Participant(models.Model):
    name=models.CharField(max_length=100,null=True)
    course=models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=70,blank=True,unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
    
    class Meta:
        verbose_name='Course Participant'
        verbose_name_plural='Course Participants'
     