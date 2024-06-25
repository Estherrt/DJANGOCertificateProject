from django.db import models

# Create your models here.
class Participant(models.Model):
    name=models.CharField(max_length=100,null=True)
    course=models.CharField(max_length=100,null=True)
    email = models.EmailField(max_length=70,blank=True,unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name='Course Participant'
        verbose_name_plural='Course Participants'
     